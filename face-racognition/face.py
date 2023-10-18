from deepface import DeepFace
import cv2
from retinaface import RetinaFace
    

img = "nigga.jpeg"

# Configura enforce_detection a False para evitar errores si no se detecta una cara
analisis = DeepFace.analyze(img_path=img, actions=["gender", "emotion", "age","race"], enforce_detection=False)

print(analisis)

# Verifica si se detectó una cara antes de mostrar los resultados
if len(analisis) > 0 and "region" in analisis[0] and analisis[0]["region"] is not None:
    img = cv2.imread(img)
    cv2.namedWindow("deteccion de emociones", cv2.WINDOW_NORMAL)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'Genero:' + analisis[0]['dominant_gender'], (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, 'Emocion:' + analisis[0]['dominant_emotion'], (10, 60), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(img, 'Edad:' + str(analisis[0]['age']), (10, 90), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    cv2.putText(img, 'Raza:' +analisis[0]['dominant_race'], (10, 120), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("deteccion de emociones", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("No se ha detectado una cara en la imagen.")
