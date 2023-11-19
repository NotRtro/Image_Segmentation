from openai import OpenAI

client = OpenAI(api_key='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')

def generateCamp(caracteristicas, title, rubro):

    data =  f"""quiero generar una campania en el rubro {rubro} y teniendo en cuenta que haciendo un analisis de los alrededores de mi negocio
            tanto en las personas que pasan por mi negocio, y como son los alrededores de este, tenemos en cuenta que la mayoria de clientes
            tienen caracteristicas principales como {caracteristicas}""" # Fixed the formatting of the string
    
    response = client.chat.completions.create(model = "gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "Eres un asistente de marketing que ayuda a las personas a crear campañas publicitarias para sus negocios con ideas creativas y factibles."},
        {"role": "user", "content": 'Que campaña me recomiendas usar para ' + data},
        #{"role": "user", "content": 'Que nombres para una campaña puedo ponerle con la tematica' + title},
    ])


    #print(response.choices[0].message.content)
    return response.choices[0].message.content

'''caracteristicas = input("Por favor, introduce las características: ")
title = input("Por favor, introduce el título: ")
rubro = input("Por favor, introduce el rubro: ")
final = generateCamp(caracteristicas, title, rubro)
print(final)

'''