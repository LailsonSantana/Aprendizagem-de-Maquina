import cv2
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

# Carregue o modelo pré-treinado
model = tf.saved_model.load('PATH_TO_SAVED_MODEL')

# Carregar o mapa de etiquetas para as categorias
category_index = label_map_util.create_category_index_from_labelmap('PATH_TO_LABELMAP.pbtxt')

# Função para carregar a imagem e converter para o formato esperado pelo modelo
def load_image_into_numpy_array(path):
    return cv2.imread(path)

# Carregar e preparar a imagem
image_np = load_image_into_numpy_array('PATH_TO_IMAGE')

# A entrada precisa ser um tensor
input_tensor = tf.convert_to_tensor(image_np)
input_tensor = input_tensor[tf.newaxis, ...]

# Realizar a detecção
detections = model(input_tensor)

# Remover dimensões extras dos resultados
num_detections = int(detections.pop('num_detections'))
detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
detections['num_detections'] = num_detections

# Detecção de caixas, classes e pontuações
detection_boxes = detections['detection_boxes']
detection_classes = detections['detection_classes']
detection_scores = detections['detection_scores']

# Visualizar os resultados
viz_utils.visualize_boxes_and_labels_on_image_array(
    image_np,
    detection_boxes,
    detection_classes,
    detection_scores,
    category_index,
    use_normalized_coordinates=True,
    max_boxes_to_draw=200,
    min_score_thresh=.30,
    agnostic_mode=False)

# Exibir a imagem com as caixas delimitadoras
cv2.imshow('Object Detection', image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
