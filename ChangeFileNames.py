import os

list_files = os.listdir(r'Images')

# Este hpt método cambia el nombre de archivos de manera masiva

count = 0
for image in list_files:
    images_path = r'Images'
    aux_name = '_MG_' + str(count) + '.jpg'
    old_name = os.path.join(os.path.dirname(__file__), images_path, image)
    new_name = os.path.join(os.path.dirname(__file__), images_path, aux_name)
    os.rename(old_name, new_name)
    count += 1


