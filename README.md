# Aplicaciones de Procesamiento de Imágenes y Generación de Campañas

Este repositorio contiene tres scripts principales desarrollados en Python que implementan funcionalidades de detección y análisis de imágenes, así como generación automática de campañas publicitarias usando IA.

## Contenido

- [`segmentacion.py`](./segmentacion.py): Segmentación y detección de objetos en imágenes usando un modelo preentrenado con OpenCV.
- [`multi-face.py`](./multi-face.py): Detección y análisis de rostros en imágenes usando RetinaFace y DeepFace.
- [`generate_campaning.py`](./generate_campaning.py): Aplicación Flask que genera recomendaciones de campañas publicitarias usando OpenAI.

---

## 1. segmentacion.py

### Descripción
Este script utiliza un modelo `Caffe` cargado mediante OpenCV para detectar objetos en imágenes estáticas (e.g., `car1.jpg`, `car2.jpg`, etc.). Se extraen las regiones detectadas según las clases seleccionadas por el usuario y se almacenan como archivos `.jpg` en un directorio temporal.

### Dependencias
- OpenCV (`cv2`)
- Flask
- Modelo `prototxt` y `caffemodel` de clasificación

### Uso
1. Define las clases de interés desde el front-end.
2. Envía una solicitud POST a `/procesar_subida`.
3. El script detecta las clases y guarda las regiones de interés (ROI) localmente.

---

## 2. multi-face.py

### Descripción
Este script permite detectar múltiples rostros en una imagen (`elite.jpg` por defecto), los guarda temporalmente y los analiza usando DeepFace para obtener edad, género, emoción y raza dominante.

### Dependencias
- `retinaface`
- `deepface`
- `opencv-python`
- `matplotlib`

### Uso
```bash
python multi-face.py
```
Los resultados se almacenan en un diccionario persons y se imprimen por consola.

##3. generate_campaning.py
###Descripción
Aplicación web basada en Flask que recibe un texto del usuario (por ejemplo, un producto o situación) y genera una recomendación de campaña usando la API de OpenAI.

###Dependencias
Flask

openai

### Requisitos

Debes definir una clave de API válida para OpenAI:

```python
import openai

openai.api_key = 'your_api_key'
