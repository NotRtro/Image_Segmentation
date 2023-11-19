from flask import request, jsonify, render_template, session,abort, redirect,url_for
from contro_mongo import *
from temp import generateCamp
import json
"""para login"""
import requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from app import app, GOOGLE_CLIENT_ID,client_secrets_file,flow
"""cierre"""

"""Para face"""
from deepface import DeepFace
from app.schemas.seg import * 
#import cv2 #segmentation
import numpy as np
import base64
from io import BytesIO
from PIL import Image 
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

def get_main_colors(imagenes, n_colors):
    result = []
    for i in imagenes:
        image = cv2.imdecode(i, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.reshape(-1, 3)

        kmeans = KMeans(n_clusters=n_colors)
        labels = kmeans.fit_predict(image)  

        counts = np.bincount(labels)
        colors = kmeans.cluster_centers_

        main_colors = (result.append(colors[i].astype(int)) for i in range(n_colors))
    return result



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
    #print(id_info)
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
    # go home
    # pasar img del usuario
    return render_template("put_image.html")


'''
- route para el login

'''



"""FACE"""
# seleccionar una opcion para el analisis de caras (una o multiples, rutas para cada una)
@app.route('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'GET':
        return render_template('put_image.html')
    else:
        data = request.files.getlist('image')
        if data is None:
            raise ValueError('No image provided')

        file_data = data[0].read()  # Lee los datos del archivo en formato bytes
        image = Image.open(BytesIO(file_data))

        # Convertir la imagen a un arreglo NumPy
        image_np = np.array(image)

        # Analizar la imagen con DeepFace
        analisis = DeepFace.analyze(image_np, actions=["gender", "emotion", "age", "race"], enforce_detection=False)
        dic = {}
        dic['Genero'] = analisis[0]['dominant_gender']
        dic['Emocion'] = analisis[0]['dominant_emotion']
        dic['Edad'] = str(analisis[0]['age'])
        dic['Rasgos'] = analisis[0]['dominant_race']
        """
        GUARDAR LAS IMAGENES CON SUS ANALISIS -
        {imagenes
            usur_id:
            ---id_img: creciend---
            vec_img: [np_array]
            
            analisis:[{...}]
        }
        """

        #return jsonify({'analysis': dic})  # usar_otro momnento

        # except Exception as e:
        #    return jsonify({'message': str(e)}), 400

        #except Exception as e:
        #    return jsonify({'message': str(e)}), 400
"""Cierre"""



"""para Segmentation"""
@app.route('/procesar_seg', methods=['GET','POST'])
def procesar_seg():
    if request.method == 'GET':
        return render_template('segmentation.html')
    else:
        # 3 post: imagenes, selected_classes (numeros separados por coma), title (tematica)
        imagenes = request.files.getlist('images[]')
        #selected_classes_json = request.form['selected_classes']  # Get the JSON string from the form data
        #selected_classes = json.loads(selected_classes_json)  # Parse the JSON string into a list
        #selected_classes = [int(class_id) for class_id in selected_classes if class_id.isdigit() and int(class_id) in classes]
        selected_classes = request.form.get('classes','')
        # pasar a lista y quitarle las comas
        selected_classes = selected_classes.split(',')
        selected_classes = [int(class_id) for class_id in selected_classes if class_id.isdigit() and int(class_id) in classes]
        selected_title = request.form.get('tematica','') # opcional
        selected_caracteristicas = request.form.get('caracteristicas','') # opcional
        selected_rubro = request.form.get('rubro','') # opcional
        labels = {}
        for im in imagenes:
            if im.filename == '':
                return redirect(request.url)

            filename = im.filename
            content_type = im.content_type
            file_data = im.read()  # Lee los datos del archivo en formato bytes

            # Ejemplo: Abrir la imagen con Pillow y cambiar su tamaño
            image = Image.open(BytesIO(file_data))
            image_np = np.array(image)

            height, width = image.size
            
            image_resized =cv2.resize(image_np, (300, 300))
            blob = cv2.dnn.blobFromImage(image_resized, 0.007843, (300,300), (127.5, 127.5, 127.5))
            net.setInput(blob)
            detections = net.forward() 
            # matrix de imagenes segmentadas 'segmentacion'
            result = []
            # diccionario para labels que aumente por cada objeto encontrado
            for detection in detections[0][0]:
                if  detection[2]>0.45:
                    label_index = int(detection[1])
                    if label_index in selected_classes:
                        if classes[label_index] not in labels:
                            labels[classes[label_index]] = 0
                        print("clase encontrada", classes[label_index])
                        labels[classes[label_index]] = labels[classes[label_index]]+1
                        box = detection[3:7] * [width, height, width, height]
                        x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])                       
                        image_np2 = np.array(image)

                        roi = image_np2[y_start:y_end, x_start:x_end]
                        
                        #result.append(roi.flatten())
                        result.append(roi.flatten())
                        """"ENVIAR TODO EL RESULTADO A LA BASE DE DATOS
                        {
                            user_id:
                            title:del front
                            images:[np_array]
                            result:
                            caracteristicas...
                        }
                        
                        """     
            print(labels)
        campaign = generateCamp(selected_caracteristicas, selected_title, selected_rubro)

        # mostrar cuanto falta del procesamiento
        # se han encontrado 4 carros........
        
        #image = (base64.b64encode(Image.open(BytesIO(i.read()))) for i in imagenes)
        #colors = get_main_colors(result, 3)
        #print(colors)
        return jsonify({'message': 'success'},{'result':labels }, {'campaign':campaign}), 200
"""cierre"""