from flask import request, jsonify, render_template, session,abort, redirect,url_for
from contro_mongo import *

"""para login"""
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app import app, GOOGLE_CLIENT_ID,client_secrets_file,flow
"""cierre"""

"""Para face"""
from deepface import DeepFace
import cv2
import numpy as np
import base64
import io
"""cierre"""

"""HTTP LOGIN"""
#app.secret_key = "CodeSpecialist.com"
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url, "/p")


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)#token de la sesion

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    """
    GUARDAR AL USUARIO EN LA BASE DE DATOS
    """
    print(id_info)
    new_user(id_info.get("sub"),id_info.get("given_name"),id_info.get("family_name"),id_info.get('email'),id_info.get("picture"))

    return redirect("protected_area")
    


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return "Hello World <a href='/login'><button>Login</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template("put_image.html")



"""FACE"""

@app.route('/analyze', methods=['GET','POST'] )
def analyze():#guardar las imagenes que se manden a la base de datos
    if request.method == 'GET':
        print('entro get')
        return render_template('put_image.html')
    else:
        try:
            print('entro en post')
            data = request.form.get('image', None)
            print(data)
            if data is None:
                raise ValueError('No image provided')

            img_data = base64.b64decode(data)
            img = cv2.imdecode(np.frombuffer(img_data, np.uint8), -1)

            # Configura enforce_detection a False para evitar errores si no se detecta una cara
            analisis = DeepFace.analyze(img_path=img, actions=["gender", "emotion", "age","race"], enforce_detection=False)
            print(analisis)
            """
                GUARDAR LAS IMAGENES CON SUS ANALISIS -
                {imagenes
                id_img: creciend
                vec_img:
                usur_id:
                analisis:{...}
            } 
            """
                
            return jsonify({'analysis': analisis})#analisis json

        except Exception as e:
            return jsonify({'message': str(e)}), 400
"""Cierre"""