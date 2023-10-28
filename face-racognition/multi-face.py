import cv2
from retinaface import RetinaFace    
import matplotlib.pyplot as plt
import os
from deepface import DeepFace

index = 0
img = "elite.jpg"
faces = RetinaFace.extract_faces(img_path=img, align=False)
persons ={}

for face in faces:
    plt.imshow(face)
    plt.savefig(f"./faces/{index}.png")  
    index +=1

for i in range(index):
    analisis = DeepFace.analyze(img_path="./faces/"+str(i)+".png", actions=["gender", "emotion", "age","race"], enforce_detection=False)
    persons[i] = ['Genero:' + analisis[0]['dominant_gender'],'Emocion:' + analisis[0]['dominant_emotion'],
                  'Edad:' + str(analisis[0]['age']),'Raza:' +analisis[0]['dominant_race']]
    os.remove("./faces/"+str(i)+".png")

print(persons)





