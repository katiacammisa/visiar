import cv2
import csv
import glob
import numpy
import math


# Escribo los valores de los momentos de Hu en el archivo
def write_hu_moments(label, writer):
    print(label)
    files = glob.glob('../pokeShapes/' + label + '/*')  # label recibe el nombre de la carpeta
    hu_moments = []
    for file in files:
        hu_moments.append(read_contour(file))
    for mom in hu_moments:
        flattened = mom.ravel()  # paso de un array de arrays a un array simple.
        row = numpy.append(flattened, label)  # le metes el flattened array y le agregas el label
        writer.writerow(row)  # Escribe una linea en el archivo.


def read_contour(file):
    contour = numpy.load(file)
    moments = cv2.moments(contour)
    huMoments = cv2.HuMoments(moments)
    for i in range(0, 7):
        huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(
            abs(huMoments[i]))
    return huMoments


def generate_hu_moments_file():
    with open('generated-files/shapes-hu-moments.csv', 'w',
              newline='') as file:  # Se genera un archivo nuevo (W=Write)
        writer = csv.writer(file)
        # Ahora escribo los momentos de Hu de cada uno de las figuras. Con el string "rectangle...etc" busca en la carpeta donde estan cada una de las imagenes
        # generar los momentos de Hu y los escribe sobre este archivo. (LOS DE ENTRENAMIENTO).
        for label in ["Bulbasor", "Ivysaur"]:
            write_hu_moments(label, writer)
