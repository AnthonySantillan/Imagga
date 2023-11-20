import os
import shutil
import requests

api_key = 'acc_19859d167cf5874'
api_secret = 'c5308149d79eaa67c9e7aa710e8666fe'
image_dir = 'C:\laragon\www\consumo-apis\imagenes'

CLASSIFICATION_PATH = 'imagenes/clasificacion/'
CATEGORIES = ['car', 'bicycle']
FILE_SEP = os.sep

def checkPaths(categories, classification_path):
    if not os.path.exists(classification_path):
        os.mkdir(classification_path)
    for category in categories:
        target_path = classification_path + category + FILE_SEP
        if not os.path.exists(target_path):
            os.mkdir(target_path)


def classifyImage(image_path, categories, classification_path):
    response = requests.post(
        'https://api.imagga.com/v2/tags',
        auth=(api_key, api_secret),
        files={'image': open(image_path, 'rb')}
    )
    if response.status_code == 200:
        data = response.json()
        filename = os.path.basename(image_path)
        for tag in data['result']['tags']:
            for category in categories:
                target_path = classification_path + category + FILE_SEP
                if tag['confidence'] == 100 and tag['tag']['en'] == category:
                    shutil.copy(image_path, target_path + filename)
    else:
        print("API error " + image_path)


checkPaths(CATEGORIES, CLASSIFICATION_PATH)

for filename in os.listdir(image_dir):
    f = os.path.join(image_dir, filename)
    if os.path.isfile(f):
        image_path = os.path.splitext(f)[0] + os.path.splitext(f)[1]
        split_path = image_path.split(FILE_SEP)
        if len(split_path) > 1:
            filename = split_path[-1]  # Using -1 index to get the last element
            classifyImage(image_path, CATEGORIES, CLASSIFICATION_PATH)
        else:
            print("No se pudo obtener el nombre de archivo de la ruta:", image_path)
            # Decide cómo manejar este caso, ya sea omitirlo o agregar lógica adicional
