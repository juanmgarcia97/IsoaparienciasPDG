from difflib import SequenceMatcher
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
    """Este método procesa una imagen con la
    API de Google Vision y devuelve los textos encontrados
    en ella.
    
    @param file_path: la ruta de la imagen a procesar
    @author Joan David Colina y Juan Martín García"""
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    finalText = refactorText(docText)
    return finalText, response

def processImageAllData(file_path):
    """Este método procesa una imagen con la 
    API de Google Vision y devuelve el nivel de
    confianza por cada uno de los caracteres
    
    @param file_path: la ruta de la imagen a procesar
    @author Joan David Colina y Juan Martín García"""
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

def refactorText(data):
    texts = data.split('\n')
    finalText = ''

    for text in texts:
        finalText = finalText + text + ';'
    return finalText

def comparisonStrings(stringA, stringB):
    resultA = stringA.split('(****)')[0].split(';')
    resultB = stringB.split('(****)')[0].split(';')
    finalResult = 0
    for charA in resultA:
        for charB in resultB:
            finalResult += SequenceMatcher(None, charA, charB).ratio()
            # print(charA, charB)
    # print("Prueba:::", stringA, stringB)
    return finalResult
    # print("Prueba:::", stringA, stringB)
    # return SequenceMatcher(None, stringA, stringB).ratio()

def findGreaterValues(values, hashMap):
    response = hashMap.get(values[0]) + ": " + str(values[0]) + "\n" + hashMap.get(values[1])+": "+ str(values[1]) + "\n"+ hashMap.get(values[2])+": "+ str(values[2])
    return response, [hashMap.get(values[0]), hashMap.get(values[1]), hashMap.get(values[2])]