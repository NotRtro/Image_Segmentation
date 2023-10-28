import pymongo

# Conecta a la base de datos MongoDB (si no existe, se creará automáticamente)
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Cambia la URL según tu configuración

# Selecciona una base de datos (si no existe, se creará automáticamente)
db = client["BDGeneral"]  # Reemplaza "mi_base_de_datos" por el nombre que desees

# Ahora puedes interactuar con tu base de datos.
