from pymongo import *


#para la coneccion
client=MongoClient('mongodb+srv://branduser:QSwaDTzWNr7FPLnP@branddb.ekim1xt.mongodb.net/') 
base_datos=client['Brand_Vista']
coleccion_usuarios=base_datos['brand_users']
coleccion_segmentation=base_datos['users_segmentation']

"""
==================================================================
                            USUARIO                      
==================================================================
"""
def user_exits(id):
    if coleccion_usuarios.find_one({"_id":id}):
        return True
    else:
        return False
    
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

"""
==================================================================
                        SEGMENTACION                      
==================================================================

def find_segmentation(id):
    if coleccion_usuarios.find_one({"_id":id}):
        return False
    else:
        return True
def new_segmentation(id,title,imagenes_array,result):
    if user_exits(id):
        coleccion_segmentation.insert_one({
            "_id":id,
            "title":title,
            "imagenes":imagenes_array,
            "result":result
        })
        print('se inserto correctamente')

"""
#coleccion_usuarios.insert_one(post).inserted_id
#new_user('1','ronaldo','flores','hola@gmail.com','1234.jpg')
#print(base_datos)

