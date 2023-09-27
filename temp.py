import os
import pathlib
import json

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
print(client_secrets_file)

temp  = json.loads('client_secret.json')
print(temp)