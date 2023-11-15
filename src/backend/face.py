from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import base64
import io
from main import *


@app.route('/analyze', methods=['POST'])
def analyze_image():#guardar las imagenes que se manden a la base de datos
    try:
        data = request.json.get('image', None)
        if data is None:
            raise ValueError('No image provided')

        img_data = base64.b64decode(data)
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), -1)

        # Configura enforce_detection a False para evitar errores si no se detecta una cara
        analisis = DeepFace.analyze(img_path=img, actions=["gender", "emotion", "age","race"], enforce_detection=False)
        print(analisis)
        """
            GUARDAR LAS IMAGENES CON SUS ANALISIS -
            {imagenes
            id_img: creciend
            vec_img:
            usur_id:
            analisis:{...}
        } 
        """
            
        return jsonify({'analysis': analisis})#analisis json

    except Exception as e:
        return jsonify({'message': str(e)}), 400
