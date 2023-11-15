import os
import pathlib
#from main import *
import requests
from flask import Flask,session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from src.backend.contro_mongo import * #data base
#from face import *
import google.auth.transport.requests

app = Flask("Google Login App")
app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "1053211312918-n0qgtnjvtp9dnqsdtksmpbhsghjs8khi.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


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


"""@app.route('/upload', methods=['POST'])
def upload_file():
    print('entraste aqui')
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(filename)
        analyze_image(filename)
        return redirect(url_for('uploaded_file', filename=filename))
"""
if __name__ == '__main__':
    app.run(debug=True)