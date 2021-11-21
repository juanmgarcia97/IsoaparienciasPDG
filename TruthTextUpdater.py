import io
import os
from tkinter.constants import TRUE
from google.cloud import vision

SPLITTER = "(****)"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceToken.json'
client = vision.ImageAnnotatorClient()

truth_text = open('test1.txt', "a")


list_files = os.listdir(r'Images')
count = 0
images_path = r'Images'
images_results = []

# for image in list_files:
#     aux_name = '_MG_' + str(count) + '.jpg'
#     file_path = os.path.join(os.path.dirname(__file__), images_path, aux_name)
#     with io.open(file_path, 'rb') as image_file:
#         content = image_file.read()

#     image = vision.Image(content=content)
#     response = client.document_text_detection(image=image)
#     docText = response.full_text_annotation.text

#     texts = docText.split('\n')
#     finalText = ''

#     for text in texts:
#         finalText = finalText + text + ';'

#     print(finalText + SPLITTER + aux_name)

#     images_results.append(finalText + SPLITTER + aux_name + '\n')
#     count += 1

# truth_text.writelines("了無")
# truth_text.close()

def existsInTruthText(image_result):
    with open('test1.txt', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    hex_result = image_result.split('(****)')[0]
    for i in lines:
        hex_new_image = i.split('(****)')[0]
        if(hex_new_image == hex_result):
            return True
    return False
