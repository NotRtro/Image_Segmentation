from flask import Flask, render_template, request, redirect
import openai
from login import app

openai.api_key = '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'
conversations = []

@app.route('/final', methods = ['GET', 'POST'])
def generateCamp():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['data']:
        data = 'Que campaña me recomiendas usar para ' + request.form['data']

        response = openai.Completion.create(
            engine = 'gpt-3.5-turbo',
            prompt = data,
            temperature = 0.5,
            max_tokens = 150,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0.6
        )
        answer = 'BrandVista: ' + response.choices[0].text.strip()

        conversations.append(data)
        conversations.append(answer)

        return render_template('index.html', chat = conversations)

    else:
        return redirect('/protected_area')