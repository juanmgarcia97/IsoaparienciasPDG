from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import VisionAPIDemo as api

root = Tk()
root.title('Isoapariencias de medicamentos inyectables')
root.geometry("500x400")
root.iconbitmap(r'Images/icons8-capsule-64.ico')

frame = LabelFrame(root, padx=2, pady=2)
frame.pack(padx=2, pady=2)
imageIso = LabelFrame(root, padx=2, pady=2)
imageIso.pack(padx=2, pady=2)
resultIso = LabelFrame(root, padx=2, pady=2)
resultIso.pack()


def openFile():
    global image_label, uploaded_image, filename
    filename = filedialog.askopenfilename(title="Seleccionar imagen")
    label = Label(imageIso, text=filename.rsplit("/")[-1]).pack()
    uploaded_image = ImageTk.PhotoImage(
        Image.open(filename).resize([200, 300]))
    image_label = Label(imageIso, image=uploaded_image).pack()
    image_label.image = uploaded_image


def findIso():
    data = api.processImage(filename)[0]
    labelData = Label(resultIso, text=data).pack()


upload_image = Button(frame, text="Cargar Imagen",
                      command=openFile).grid(row=0, column=0)
chose_med = Button(frame, text="Elegir medicamento").grid(row=2, column=0)
delete_image = Button(frame, text="Eliminar imagen").grid(row=1, column=1)
find_iso = Button(frame, text="Encontrar isoapariencias",
                  command=findIso).grid(row=1, column=2)
gen_report = Button(frame, text="Generar reporte").grid(row=1, column=3)

root.mainloop()
