from zenora import APIClient
from flask import Flask, render_template, request, session, redirect
from config import *
import requests
import zenora

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a48a13b2a21f410aa53641279dd9bfcad9d15761f4724e68'
##client = APIClient(DISCORD_TOKEN)
#TOKEN = TOKEN

@app.route('/')
def homepage():
    return render_template('index.html', url=oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': 'identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(f'https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
    r.raise_for_status()
    session['token'] = r.json()['access_token']

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """
    client = APIClient(
        TOKEN,
        client_secret= client_secret,
    )
    access_token = client.oauth.get_access_token(code=, redirect_uri=oauth_url).access_token
    bearer_client = APIClient(access_token, bearer=True)
    me = bearer_client.get_current_user()
    """
    token = 'null'

    if session.get('access_token'):
        token = session['access_token']

    return render_template('dashboard.html', user=token)

#test oli    
#?

if __name__ == '__main__':
    app.run(debug=True) 
