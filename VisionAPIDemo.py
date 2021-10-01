import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceToken.json'
client = vision.ImageAnnotatorClient()

FOLDER_PATH = r'C:\Users\juanm\Documents\ICESI\9no\Proyecto de Grado I\Proyecto\Codigo\GoogleVisionDemo\Images'
IMAGE_FILE = 'testImage.jpeg'
FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)

with io.open(FILE_PATH, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.document_text_detection(image=image)

docText = response.full_text_annotation.text
print(docText)


pages = response.full_text_annotation.pages
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
