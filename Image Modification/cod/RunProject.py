"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Image Resizing", autori S. Avidan si A. Shamir
"""

from Resize_Image import *
import matplotlib.pyplot as plt

image_name = '../data/tall.jpg'
params = Parameters(image_name)

# seteaza optiunea de redimenionare
# micsoreazaLatime, micsoreazaInaltime, maresteLatime, maresteInaltime, amplificaContinut, eliminaObiect
params.resize_option = 'micsoreazaInaltime'
# numarul de pixeli pe latime
params.num_pixels_width = 100
# numarul de pixeli pe inaltime
params.num_pixel_height = 100
# afiseaza drumul eliminat
params.show_path = True
# metoda pentru alegerea drumului
# aleator, greedy, programareDinamica
params.method_select_path = 'aleator'

resized_image = resize_image(params)
resized_image_opencv = cv.resize(params.image, (resized_image.shape[1], resized_image.shape[0]))

f, axs = plt.subplots(2, 2, figsize=(15, 15))
plt.subplot(1, 3, 1)
plt.imshow(params.image[:, :, [2, 1, 0]])
plt.xlabel('original')

plt.subplot(1, 3, 2)
plt.imshow(resized_image_opencv[:, :, [2, 1, 0]])
plt.xlabel('OpenCV')

plt.subplot(1, 3, 3)
plt.imshow(resized_image[:, :, [2, 1, 0]])
plt.xlabel('My result')
plt.show()


