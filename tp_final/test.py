import cv2 as cv
import numpy as np

from scrapper import saveImageFromUrl
from details import getPokemonData


def getPokeContours(pokeDict):
    # pokeDict = getPokemonData()
    list = []
    for n in range(2):
        url = pokeDict.get(n).image
        saveImageFromUrl(n, url)
        image = cv.imread(f'./images/{n}.png')
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        # TODO Le setteamos un valor a la trackbar
        ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        # Saving the array in a text file
        # np.savetxt(f'./pokeContours/{n}.csv', contours[0], delimiter=',')
        # file = open(f'./pokeContours/{n}.txt', 'w+')
        # content = contours[0]
        # file.write(content)
        # file.close()
        # TODO NOS PONE LOS 3 PUNTITOSSSS
        list.append(contours[0])
    return list
