from flask import Flask
"""para login"""
import os
import pathlib
from google_auth_oauthlib.flow import Flow
"""cierre"""


"""para login"""
app=Flask(__name__)
app.secret_key = "CodeSpecialist.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "1053211312918-n0qgtnjvtp9dnqsdtksmpbhsghjs8khi.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)
"""cierre"""



from app.routes import *