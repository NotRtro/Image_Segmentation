from flask import Flask, render_template, request, redirect
import openai
from login import app

openai.api_key = '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'

@app.route('/final', methods = ['GET', 'POST'])
def generateCamp():
    if request.method == 'GET':
        return render_template('index.html')
    if request.form['data']:
        data = 'Que campaña me recomiendas usar para ' + request.form['data']

        response = openai.ChatCompletion.create(
            engine = "gpt-4-0314",
            prompt = data,
            temperature=0.5,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )

        answer = 'BrandVista: ' + response.choices[0].text.strip()

        return render_template('index.html', chat = answer)

    else:
        return redirect('/protected_area')
