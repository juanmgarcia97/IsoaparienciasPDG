import os
import io
# para realizar los reportes en excel necesitamos la siguiente libreria
import openpyxl
# para instalar la api de google y pandas se debe usar los siguientes comandos desde poweshell (estando dentro del proyecto python):
# py -m pip install google.cloud.vision
# py -m pip install pandas
from openpyxl.styles import Alignment
import VisionAPI as apiText

FOLDER_PATH = r'Images'

list = os.listdir(FOLDER_PATH)

wb = openpyxl.Workbook()
# para acceder a la hoja activa usamos el atributo "active"
hoja = wb.active
hoja.title = "Reporte"

hoja["A1"] = "Nombre de la imagen"
hoja["B1"] = "Resultado tabla de verdad"
hoja["C1"] = "Isoapariencia 1"
hoja["D1"] = "Isoapariencia 2"
hoja["E1"] = "Isoapariencia 3"

pointer = 2

with open('truthText.txt', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    def __init__(self):
        self.store = [None for _ in range(16)]

    def get(self, key):
        index = hash(key) & 15
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None

    def put(self, key, value):
        nd = Node(key, value)
        index = hash(key) & 15
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd


hm = HashMap()


for x in range(0, 250, 5):
    EXCEL_POSITION_IMAGE_NAME = "A"+str(pointer)
    EXCEL_POSITION_RESULT_TRUTH_TEXT = "B"+str(pointer)
    EXCEL_POSITION_ISO_1 = "C"+str(pointer)
    EXCEL_POSITION_ISO_2 = "D"+str(pointer)
    EXCEL_POSITION_ISO_3 = "E"+str(pointer)

    IMAGE_FILE = "_MG_"+str(x)+".jpg"
    SCRIPT_DIR = os.path.dirname(__file__) + '\Images'
    FILE_PATH = os.path.join(SCRIPT_DIR, IMAGE_FILE)

    data = apiText.processImage(FILE_PATH)[0]
    values = []
    for i in lines:
        arr = i.split('(****)')
        img_name = arr[1].rstrip()
        if img_name != IMAGE_FILE:
            # print(arr[1])
            comparison = apiText.comparisonStrings(data, arr[0])
            hm.put(comparison, img_name)
            values.append(comparison)

        # values = cv2.sort(values)
    values.sort(reverse=True)
    print(len(values))
    result_values, image_names = apiText.findGreaterValues(values, hm)

    response = result_values.split('\n')

    hoja[EXCEL_POSITION_IMAGE_NAME] = IMAGE_FILE
    hoja[EXCEL_POSITION_RESULT_TRUTH_TEXT] = lines[x]
    hoja[EXCEL_POSITION_ISO_1] = str(response[0])
    hoja[EXCEL_POSITION_ISO_2] = str(response[1])
    hoja[EXCEL_POSITION_ISO_3] = str(response[2])
    # apiText.processImage()

    pointer += 1

wb.save('firstTry.xlsx')
