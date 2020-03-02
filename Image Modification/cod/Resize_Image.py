import sys
import cv2 as cv
import numpy as np

from Parameters import *
from SelectPath import *

import pdb


def compute_energy(img):
    """
    calculeaza energia la fiecare pixel pe baza gradientului
    :param img: imaginea initiala
    :return:E - energia

    E[0] e la fel cu E[0,:]
    Laur: c = np.argmin(E[0,:])
    for i in range (1, E.shape?(n?))

    faci schema cu
    aici esti tu ->  []
    aici mergi    -1 0 1
    (cu greedy)
    """
    # urmati urmatorii pasi:
    # 1. transformati imagine in grayscale
    # 2. folositi filtru sobel pentru a calcula gradientul in directia X si Y
    # 3. calculati magnitudinea imaginii

    img_gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY);

    #de cautat totusi si codul pt SOBEL pe net
    grad_x = cv.Sobel(img_gray_scale, ddepth = cv.CV_16S, dx = 1, dy = 0, borderType = cv.BORDER_CONSTANT)
    grad_y = cv.Sobel(img_gray_scale, ddepth = cv.CV_16S, dx = 0, dy = 1, borderType = cv.BORDER_CONSTANT)

#E repr gradientii aka cat se sch un pixel de la unul la altul
    E = abs(grad_x) + abs(grad_y)
    # print(grad_y)
    # print(grad_x)

    cv.imwrite("poza.jpg", E)
    return E


def show_path(img, path, color):
    new_image = img.copy()
    for row, col in path:
        new_image[row, col] = color

    cv.imshow('path', np.uint8(new_image))
    cv.waitKey(100)




def decrease_width(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path)
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path(img, path)

    cv.destroyAllWindows()
    return img


def delete_object(params: Parameters, num_pixels, r):
    img = params.image.copy()  # copiaza imaginea originala
    img_destroy = img.copy()
    # r contine informatii pentru indicii din coltul stanga sus(x1, y1) respectiv dreapta jos al imaginii (x2, y2)
    # x1 = r[0], y1 = r[1], x2 = r[0]+r[2], y2 = r[1] + r[3]

    paths = []
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img_destroy)
        # in interiorul selectiei dau valori negative apoi voi folosi functia de reducere a latimii pentru a
        # elimina obiectul selectat
        for i in range(r[1], r[1]+r[3]):
            for j in range(r[0], r[0]+r[2]):
                E[i][j] = int(-100)
                # overflow daca dau valori prea mici, mai ales pentru poze de dimensiuni mari
        path = select_path(E, params.method_select_path)
        paths.append(path)

        if params.show_path:
            show_path(img_destroy, path, params.color_path)

        img_destroy = delete_path(img_destroy, path)



    cv.destroyAllWindows()

    return img_destroy

def decrease_height(params: Parameters, num_pixels):
    # aceeasi functie ca la decrease_width, doar ca rotim imaginea
    img1 = params.image.copy()  # copiaza imaginea originala
    img = cv.rotate(img1, cv.ROTATE_90_CLOCKWISE) # imaginea pe care voi lucra, intoarsa

    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path)
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path(img, path)
    img2 = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE) #intoarcem imaginea la pozitia originala
    cv.destroyAllWindows()
    return img2


def delete_path(img, pathway):
    """
     elimina drumul vertical din imagine
    :param img: imaginea initiala
    :pathway - drumul vertical
    return: updated_img - imaginea initiala din care s-a eliminat drumul vertical
    """
    updated_img = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = pathway[i][1]
        # copiem partea din stanga
        updated_img[i, :col] = img[i, :col].copy()
        # copiem partea din dreapta
        updated_img[i, col:] = img[i, col + 1:].copy()
        # completati aici codul vostru

    return updated_img

def add_path(img, pathway):


    updated_img = np.zeros((img.shape[0], img.shape[1] + 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = pathway[i][1]
        # copiem partea din stanga
        updated_img[i, :col] = img[i, :col].copy()
        # adaugam linia
        updated_img[i, col] = img[i, col].copy()
        updated_img[i, col + 1] = img[i, col].copy()

        # copiem partea din dreapta
        updated_img[i, col + 1:] = img[i, col:].copy()


    return updated_img


def increase_img_w(params: Parameters, num_pixels_width):
    # lucrez cu doua imagini, una de marit pe care o voi intoarce
    # si una de micsorat din care imi scot path-urile de dublat
    img = params.image.copy()  # copiaza imaginea originala
    img_destroy = img.copy()  # mai facem o copie
    paths = []  # aici retinem drumurile de dublat
    for i in range(num_pixels_width):
        # print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels_width))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img_destroy)

        # alegem drumurile exact ca la decrease_width
        drum = select_path(E, params.method_select_path)
        paths.append(drum)
        if params.show_path:
            show_path(img_destroy, drum, params.color_path)

        img_destroy = delete_path(img_destroy, drum)

    # dupa ce avem drumurile, acestea au indici diferiti fata de imaginea pe care vrem sa o marim
    # cum algoritmul sterge prin shiftare la stanga incepanddin partea dreapta a drumului
    # adaugam cate un 1 pentru pozitiile din dreapta drumului la fiecare drum intalnit

    for path in paths:
        for i in range(num_pixels_width):
            for j in range(i + 1, E.shape[1]):
                if path[j][0] == path[i][0] and path[j][1] > path[i][1]:
                    print(path[j][1])
    # cel putin asta incerc sa fac

    # acum ca avem indicii corecti(teoretic) putem adauga drumuri
    for path in paths:
        img = add_path(img, path)
    cv.destroyAllWindows()

    return img

def increase_img_h(params: Parameters, num_pixels_width):
    # acelasi algortitm ca la increase_img_w doar ca rasturnam imaginea
    img1 = params.image.copy() # copiaza imaginea originala
    img = cv.rotate(img1, cv.ROTATE_90_CLOCKWISE) # rasturnam

    img_destroy = img.copy()  # mai facem o copie
    paths = []  # aici retinem drumurile de dublat
    for i in range(num_pixels_width):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels_width))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img_destroy)

        # alegem drumurile exact ca la decrease_width
        drum = select_path(E, params.method_select_path)
        paths.append(drum)
        if params.show_path:
            show_path(img_destroy, drum, params.color_path)

        img_destroy = delete_path(img_destroy, drum)

    # actualizare indici
    for path in paths:
        for i in range(num_pixels_width):
            for j in range(i + 1, E.shape[1]):
                if path[j][0] == path[i][0] and path[j][1] > path[i][1]:
                    path[j][1] += 1


    # acum ca avem indicii corecti(teoretic) putem adauga drumuri
    for path in paths:
        img = add_path(img, path)

    img2 = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)  # intoarcem imaginea la pozitia originala
    cv.destroyAllWindows()

    return img2



def resize_image(params: Parameters):

    if params.resize_option == 'micsoreazaLatime':
        # redimensioneaza imaginea pe latime
        resized_image = decrease_width(params, params.num_pixels_width)
        return resized_image
    elif params.resize_option == 'micsoreazaInaltime':
        # redimensioneaza imaginea pe inaltime
        resized_image = decrease_height(params, params.num_pixel_height)
        return resized_image
    elif params.resize_option == 'maresteLatime':
        resized_image = increase_img_w(params, params.num_pixels_width)
        return resized_image
    elif params.resize_option == 'maresteInaltime':
        resized_image = increase_img_h(params, params.num_pixel_height)
        return resized_image
    elif params.resize_option == 'amplificaContinut':
        # amplifica continutul imaginii
        pass
    elif params.resize_option == 'eliminaObiect':
        # luam imaginea si preluam selectia
        im = params.image.copy()

        fromCenter = False
        r = cv.selectROI(im, fromCenter)
        resized_image = delete_object(params, r[2], r)

        return resized_image
    else:
        print('The option is not valid!')
        sys.exit(-1)