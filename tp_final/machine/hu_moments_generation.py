import cv2
import csv
import glob
import numpy
import math

from details import getPokemonData


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
        for label in getLabels():
            write_hu_moments(label, writer)


def getLabels():
    labels = []
    brokenIndexes = [99, 100, 52, 61, 149, 148, 145, 144, 143, 141, 135, 130, 129, 126, 125, 124, 123, 121, 118, 117,
                     112, 111, 109, 108, 98, 92, 91, 84, 83, 77, 76, 51, 48, 40, 37, 33, 25, 21, 5, 4, 54, 55, 58, 62,
                     66, 67, 73, 74]
    pokeDict = getPokemonData()
    for i in range(150):
        if i in brokenIndexes: continue
        labels.append(pokeDict.get(i).name)

    return labels
