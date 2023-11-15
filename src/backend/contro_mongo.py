from pymongo import *


#para la coneccion
client=MongoClient('mongodb+srv://branduser:qE7uLk4HfkI8oMhL@branddb.ekim1xt.mongodb.net/') 
base_datos=client['Brand_Vista']
coleccion_usuarios=base_datos['brand_users']


def find_user(id):
    if coleccion_usuarios.find_one({"_id":id}):
        return False
    else:
        return True

def new_user(id,first_name,last_name,email,picture):
    if find_user(id):
        coleccion_usuarios.insert_one({
            "_id":id,
            "first_name":first_name,
            "last_name":last_name,  
            "email":email,
            "picture":picture
        })
        print('se inserto correctamente')


#coleccion_usuarios.insert_one(post).inserted_id
#new_user('1','ronaldo','flores','hola@gmail.com','1234.jpg')
#print(base_datos)

