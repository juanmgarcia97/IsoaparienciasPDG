from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import os
import VisionAPIDemo as api

# Creación de la pantalla principal de la aplicación.
root = Tk()
root.title('Isoapariencias de medicamentos inyectables')
root.geometry("500x400")
root.iconbitmap(r'Images/icons8-capsule-64.ico')

# Creación de marco para encerrar los botones principales.
frame = LabelFrame(root, padx=2, pady=2)
frame.pack(padx=2, pady=2)

# Creación de marco para mostrar el resultado de Google Vision.
resultIso = LabelFrame(root, padx=2, pady=2)
resultIso.pack()

bottle_types = ["Agua", "Jugo", "Gaseosa", "Té", "Malta",
                "Lácteos", "Aceites", "Café", "Enjuague bucal", "Salsa", "Suero"]

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

# Método para buscar las isoapariencias usando la imagen cargada.


def findIso():
    data = api.processImage(filename)[0]
    labelData = Label(resultIso, text=data)
    labelData.pack()

# Método para eliminar la(s) imagen(es) cargada(s).


def deleteImage():
    imageIso.destroy()

# Método para abrir nueva ventana para elegir botella.


def openWindow():
    global comboType, combo, newWindow
    newWindow = Toplevel(root)
    newWindow.title("Escoger medicamento")
    newWindow.geometry("200x200")
    combo = ttk.Combobox(newWindow, values=bottle_types)
    combo['state'] = "readonly"
    combo.bind("<<ComboboxSelected>>", pickBottle)
    combo.pack()
    comboType = ttk.Combobox(newWindow)
    comboType['state'] = "readonly"
    comboType.bind("<<ComboboxSelected>>", selectImage)
    comboType.pack()
    print(list)


# Método para asignar las imágenes disponibles según el tipo de botella.
def pickBottle(event):
    global path
    if combo.get() == 'Agua':
        path = r'Images/Agua'
        list = os.listdir(path)
        comboType.config(values=list)


def selectImage(event):
    newWindow.destroy()
    image_name = comboType.get()
    data = api.processImage(path + image_name)[0]
    labelData = Label(resultIso, text=data)
    labelData.pack()


# Creación de los botones con las funciones principales de la aplicación.
upload_image = Button(frame, text="Cargar Imagen",
                      command=openFile).grid(row=0, column=0)
chose_med = Button(frame, text="Elegir botella",
                   command=openWindow).grid(row=2, column=0)
delete_image = Button(frame, text="Eliminar imagen",
                      command=deleteImage).grid(row=1, column=1)
find_iso = Button(frame, text="Encontrar isoapariencias",
                  command=findIso).grid(row=1, column=2)
gen_report = Button(frame, text="Generar reporte").grid(row=1, column=3)

# Llamado de la ventana principal para que permanezca abierta mientras la aplicación está corriendo.
root.mainloop()
