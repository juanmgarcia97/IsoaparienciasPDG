import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd

#para instalar la api de google y pandas se debe usar los siguientes comandos desde poweshell (estando dentro del proyecto python): 
# py -m pip install google.cloud.vision
# py -m pip install pandas

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceToken.json'
client = vision.ImageAnnotatorClient()

# FOLDER_PATH = r'C:\Users\juanm\Documents\ICESI\9no\Proyecto de Grado I\Proyecto\Codigo\GoogleVisionDemo\Images'
# IMAGE_FILE = 'testImage.jpeg'
# FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

def processImage(file_path):
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    return docText, response

def processImageAllData(file_path):
    pages = processImage(file_path)[1].pages
    for page in pages:
        for block in page.blocks:
            print('block confidence:', block.confidence)

            for paragraph in block.paragraphs:
                print('paragraph confidence:', paragraph.confidence)

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])

                    print('Word text: {0} (confidence: {1}'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {0} (confidence: {1}'.format(
                            symbol.text, symbol.confidence))
