from tkinter import *
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
import os
import cv2 #py -m  pip install opencv-python
import VisionAPIDemo as apiText
import VisionAPIForms as apiImg
import TruthTextUpdater as verifier

# Creación de la pantalla principal de la aplicación.
root = Tk()
root.title('Isoapariencias de medicamentos inyectables')
root.iconbitmap(r'Icons/icons8-capsule-64.ico')
root.geometry("500x600")

# Aquí estoy intentando que la aplicación se abra en la mitad de la pantalla
# app_width = 500
# app_height = 500

# screen_width = root.winfo_width()
# screen_height = root.winfo_height()
# print(screen_width)
# print(screen_height)

# x = (screen_width / 2) - (app_width / 2)
# y = (screen_height / 2) - (app_height / 2)

# root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# Creación de marco para encerrar los botones principales.
frame = LabelFrame(root, padx=2, pady=2)
frame.pack(padx=2, pady=2)

# Método para cargar una imagen y mostrarla en debajo del marco principal.


def openFile():
    global filename, imageIso
    filename = filedialog.askopenfilename(title="Seleccionar imagen")
    imageIso = LabelFrame(root, padx=2, pady=2)
    imageIso.pack(padx=2, pady=2)
    label = Label(imageIso, text=filename.rsplit("/")[-1])
    label.pack()
    uploaded_image = ImageTk.PhotoImage(
        Image.open(filename).resize([200, 300]))
    # images_list.append(uploaded_image)
    image_label = Label(imageIso, image=uploaded_image)
    image_label.pack()
    image_label.image = uploaded_image

# Método para buscar las similitudes en los textos usando la imagen cargada.


def findIsoText():
    global better_image, resultIso
    deleteResultIsoFrame()
    # Creación de marco para mostrar el resultado de Google Vision.
    resultIso = LabelFrame(root, padx=2, pady=2)
    resultIso.pack()
    labelData = Label(resultIso)
    data = apiText.processImage(filename)[0]
    hm = HashMap()
    values = []
    image_selected = filename.split('/')[-1]

    with open('truthText.txt', encoding='utf-8', errors='ignore') as f:
        
        lines = f.readlines()
        # print(lines)
        
            
    # try:
            # array = lines.split('\n')
    for i in lines:
        arr = i.split('(****)')
        img_name = arr[1].rstrip()
        if img_name != image_selected:
            # print(arr[1])
            hm.put(apiText.comparisonStrings(data, arr[0]), img_name)
            values.append(apiText.comparisonStrings(data, arr[0]))
        
        # values = cv2.sort(values)
    values.sort(reverse=True)

    result_values, image_names = apiText.findGreaterValues(values, hm)
    better_image = os.path.join(os.path.dirname(__file__) + '\Images' , image_names[0])
    for image in image_names:
        general_path = os.path.dirname(__file__) + '\Images' 
        image_path = os.path.join(general_path, image.split(':')[0])
        # print(image.split(' ')[0])
        # img = ImageTk.PhotoImage(Image.open(image_path).resize([200, 300]))
        # img_label = Label(resultIso, image=img)
        # img_label.image = img
        # img_label.pack()
    labelData = Label(resultIso)
    labelData.config(text=result_values)
    labelData.pack()
    # except:
    #     messagebox.showerror("Sin imagen", "¡Debes cargar una imagen primero!")

def deleteResultIsoFrame():
    try:
        resultIso.destroy()
    except:
        pass

# Método para buscar las similitudes en las imágenes usando dos imágenes cargadas.
def findIsoImg():
    # try:
        
        data = apiImg.findIsoappearances(
            filename1=filename, filename2=better_image)
        print(filename, better_image)
        image = cv2.imshow("", data)
        labelData = Label(resultIso, image=image)
        labelData.pack()
    # except:
    #     messagebox.showerror(
    #         "Sin imágenes", "¡Debes cargar dos imágenes para seguir!")


# Método para eliminar la(s) imagen(es) cargada(s).


def deleteImage():
    try:
        imageIso.destroy()
        resultIso.destroy()
    except:
        messagebox.showinfo("Error al eliminar", "¡No hay nada para eliminar!")
# Método para abrir nueva ventana para elegir botella.


def openWindow():
    # global comboType, combo, newWindow
    # newWindow = Toplevel(root)
    # newWindow.title("Escoger medicamento")
    # newWindow.geometry("200x200")
    # combo = ttk.Combobox(newWindow, values=bottle_types)
    # combo['state'] = "readonly"
    # combo.bind("<<ComboboxSelected>>", pickBottle)
    # combo.pack()
    # comboType = ttk.Combobox(newWindow)
    # comboType['state'] = "readonly"
    # try:
    #     comboType.bind("<<ComboboxSelected>>", selectImage)
    # except:
    #     messagebox.showinfo(
    #         "Sin imágenes", "No hay imágenes disponibles en el momento.")
    # comboType.pack()
    # print(list)
    new_image = filedialog.askopenfilename(title="Seleccionar nueva imagen")
    new_image_name = new_image.split('/')[-1]
    result_vision = apiText.processImage(new_image)[0] + "(****)" + new_image_name
    # print(result_vision)
    # print(verifier.existsInTruthText(result_vision))
    if(not verifier.existsInTruthText(result_vision)):
        try:
            with open("test1.txt", "a") as file:
                file.write(result_vision + "\n")
            messagebox.showinfo("Exito","La imagen: " + new_image_name + " se ha agregado correcctamente a la tabla de verdad en la ultima posicion!")
        except:
            messagebox.showerror("Error","No se ha podido guarda la imagen")
    else:
        messagebox.showerror("Error", "La imagen ya se encuentra en la tabla de verdad")



# Método para asignar las imágenes disponibles según el tipo de botella.
# def pickBottle(event):
#     global path
#     path = r'Images'
#     list = os.listdir(path)
#     comboType.config(values=list)


# def selectImage(event):
#     newWindow.destroy()
#     image_name = comboType.get()
#     data = apiText.processImage(path + image_name)[0]
#     labelData = Label(resultIso, text=data)
#     labelData.pack()


# Creación de los botones con las funciones principales de la aplicación.
upload_image = Button(frame, text="Cargar Imagen",
                      command=openFile).grid(row=0, column=0)
chose_med = Button(frame, text="+ Imagen DB",
                   command=openWindow).grid(row=2, column=0)
delete_image = Button(frame, text="Eliminar imagen",
                      command=deleteImage).grid(row=1, column=1)
find_iso_text = Button(frame, text="Encontrar similitudes (texto)",
                       command=findIsoText).grid(row=0, column=2)
find_is_img = Button(frame, text="Encontrar similitudes (img)",
                     command=findIsoImg).grid(row=2, column=2)
gen_report = Button(frame, text="Generar reporte").grid(row=1, column=3)

# https://stackoverflow.com/questions/8703496/hash-map-in-python

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

# Llamado de la ventana principal para que permanezca abierta mientras la aplicación está corriendo.
root.mainloop()

