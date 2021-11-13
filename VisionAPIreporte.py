import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd
#para realizar los reportes en excel necesitamos la siguiente libreria
import openpyxl
#para instalar la api de google y pandas se debe usar los siguientes comandos desde poweshell (estando dentro del proyecto python): 
# py -m pip install google.cloud.vision
# py -m pip install pandas
from openpyxl.styles import Alignment


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceToken.json'
client = vision.ImageAnnotatorClient()

# PATH DEL AMBIENTE LOCAL DE JUAN
# FOLDER_PATH = r'C:\Users\juanm\Documents\ICESI\9no\Proyecto de Grado I\Proyecto\Codigo\GoogleVisionDemo\Images'

# PATH DEL AMBIENTE LOCAL DE JOAN 
# FOLDER_PATH = r'C:\Users\Joan Colina\Desktop\miCosas\Semestre9\PDG\proyectoClonado\IsoaparienciasPDG\Images\Agua'

FOLDER_PATH = r'Images/Agua'



list = os.listdir(FOLDER_PATH)
number_files = len(list)
print(number_files)

#Para crear un nuevl libro usamos el comando
wb = openpyxl.Workbook()
#para acceder a la hoja activa usamos el atributo "active"
hoja = wb.active
hoja.title="Reporte Prueba"
print(f'Hoja activa: {wb.active.title}')
hoja["A1"]="RESULTADO DE GOOGLE VISION"
hoja["B1"]="NOMBRE DE LA IMAGEN"
hoja["C1"]="RUTA DE LA IMAGEN"
excel_cell=2

for x in range(number_files):
    EXCEL_POSITION_GOOGLE_VISION="A"+str(excel_cell)
    EXCEL_POSITION_IMAGE_NAME="B"+str(excel_cell)
    EXCEL_POSITION_IMAGE_PATH="C"+str(excel_cell)
    excel_cell=excel_cell+1
    IMAGE_FILE = "_MG_"+str(x)+".JPG"
    SCRIPT_DIR = os.path.dirname(__file__) + '\Images\Agua'
    FILE_PATH = os.path.join(SCRIPT_DIR, IMAGE_FILE)
    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text

    texts = docText.split('\n')
    finalText = ''

    for text in texts:
        finalText = finalText + text + ';'

    currentCell = hoja[EXCEL_POSITION_GOOGLE_VISION]
    currentCell.alignment = Alignment(horizontal='center',vertical='center')
    currentCell = hoja[EXCEL_POSITION_IMAGE_NAME]
    currentCell.alignment = Alignment(horizontal='center',vertical='center')
    currentCell = hoja[EXCEL_POSITION_IMAGE_PATH]
    currentCell.alignment = Alignment(horizontal='center',vertical='center')
    hoja[EXCEL_POSITION_GOOGLE_VISION] = finalText
    hoja[EXCEL_POSITION_IMAGE_NAME] = IMAGE_FILE
    hoja[EXCEL_POSITION_IMAGE_PATH] = FILE_PATH
    

#Para guardar un archivo excel usamos el metodo save
wb.save('reportePruebas.xlsx')










'''
pages = response.full_text_annotation.text
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
                        symbol.text, symbol.confidence))'''


