import glob
import pathlib
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
# Usaremos estas herramientas del Object Detection API para visualizar las detecciones
from object_detection.utils import ops
from object_detection.utils import visualization_utils as viz
from object_detection.utils.label_map_util import create_category_index_from_labelmap

model = hub.load('https://tfhub.dev/tensorflow/mask_rcnn/inception_resnet_v2_1024x1024/1')

def load_image(path):
    """
    Carga una imagen en formato NumPy dada su ruta en disco.
    :param path: Ruta a la imagen a cargar.
    :return: Imagen en formato NumPy.
    """

    # Lee la imagen.
    image_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(image_data))

    # Definimos las dimensiones de un lote de una sola imagen en formato RGB.
    width, height = image.size
    shape = (1, height, width, 3)

    # Redimensiona el arreglo.
    image = np.array(image.getdata())
    image = image.reshape(shape).astype('uint8')

    return image

def load_image(path):
    """
    Carga una imagen en formato NumPy dada su ruta en disco.
    :param path: Ruta a la imagen a cargar.
    :return: Imagen en formato NumPy.
    """

    # Lee la imagen.
    image_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(image_data))

    # Definimos las dimensiones de un lote de una sola imagen en formato RGB.
    width, height = image.size
    shape = (1, height, width, 3)

    # Redimensiona el arreglo.
    image = np.array(image.getdata())
    image = image.reshape(shape).astype('uint8')

    return image
def get_and_save_predictions(model, image_path):
    # Carga la imagen.
    image = load_image(image_path)

    # Pasa la imagen por el detector.
    results = model(image)

    # Convierte los resultados del detector como arreglos de NumPy.
    model_output = {k: v.numpy() for k, v in results.items()}

    # Extrae las máscaras correspondiente a la segmentación de cada objeto detectado.
    detection_masks = model_output['detection_masks'][0]
    detection_masks = tf.convert_to_tensor(detection_masks)

    # Extrae las coordenadas de las detecciones.
    detection_boxes = model_output['detection_boxes'][0]
    detection_boxes = tf.convert_to_tensor(detection_boxes)

    # Traduce las máscaras de las cajas a las imágenes.
    detection_masks_reframed = ops.reframe_box_masks_to_image_masks(detection_masks,
                                                                    detection_boxes,
                                                                    image.shape[1],
                                                                    image.shape[2])

    # Binariza las máscaras.
    detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)

    model_output['detection_masks_reframed'] = detection_masks_reframed.numpy()

    # Extrae la ubicación de las detecciones (boxes), las clases a las que pertenecen (classes) y la probabilidad
    # de cada una (scores).
    boxes = model_output['detection_boxes'][0]
    classes = model_output['detection_classes'][0].astype('int')
    scores = model_output['detection_scores'][0]
    masks = model_output['detection_masks_reframed']

    # Usa los valores retornados por el detector para crear la visualización.
    clone = image.copy()
    viz.visualize_boxes_and_labels_on_image_array(image=clone[0],
                                                  boxes=boxes,
                                                  classes=classes,
                                                  scores=scores,
                                                  category_index=category_index,
                                                  use_normalized_coordinates=True,
                                                  max_boxes_to_draw=200,
                                                  min_score_thresh=0.30,
                                                  agnostic_mode=False,
                                                  instance_masks=masks,
                                                  line_thickness=5)

    # Guarda el resultado en disco.
    plt.figure(figsize=(24, 32))
    plt.imshow(clone[0])
    output_path = str(pathlib.Path().absolute() / 'output' / image_path.split('/')[-1])
    plt.savefig(f'{output_path}')

labels_path = './resources/mscoco_label_map.pbtxt'
category_index = create_category_index_from_labelmap(labels_path)
# Corremos el detector por todas las imágenes de prueba, guardando el resultado en disco.
test_images_pattern = str(pathlib.Path().absolute().parent / '*.jpg')
for image_path in glob.glob(test_images_pattern):
    get_and_save_predictions(model, image_path)
