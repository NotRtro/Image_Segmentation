from zenora import APIClient
from flask import Flask, render_template, request
from config import *
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html', url=oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'identify'

    }
    return f'<h1>{code}</h1>'

if __name__ == '__main__':
    app.run(debug=True)
