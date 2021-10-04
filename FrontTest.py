from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

root = Tk()
root.title('Isoapariencias de medicamentos inyectables')
root.geometry("500x400")


def rcpath(rel_path):
    return os.path.join(os.getcwd(), rel_path)


root.iconbitmap(rcpath('Images/icons8-capsule-64.ico'))

frame = LabelFrame(root, padx=2, pady=2)
frame.pack(padx=2, pady=2)
frame2 = LabelFrame(root, padx=2, pady=2)
frame2.pack(padx=2, pady=2)


def openFile():
    global image_label
    filename = filedialog.askopenfilename(
        title="Seleccionar imagen", filetypes=(("PNG Files", "*.png"), ("All files", "*.*")))
    label = Label(frame2, text=filename).pack()
    uploaded_image = ImageTk.PhotoImage(Image.open(filename))
    image_label = Label(frame2, image=upload_image).pack()


upload_image = Button(frame, text="Cargar Imagen",
                      command=openFile).grid(row=0, column=0)
chose_med = Button(frame, text="Elegir medicamento").grid(row=2, column=0)
delete_image = Button(frame, text="Eliminar imagen").grid(row=1, column=1)
find_iso = Button(frame, text="Encontrar isoapariencias").grid(row=1, column=2)
gen_report = Button(frame, text="Generar reporte").grid(row=1, column=3)

root.mainloop()
