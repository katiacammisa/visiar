import cv2 as cv
import numpy as np

from scrapper import saveImageFromUrl
from details import getPokemonData


def savePokeCountours():
    pokeDict = getPokemonData()
    list = []
    for n in range(150):
        url = pokeDict.get(n).image
        saveImageFromUrl(n, url)
        image = cv.imread(f'./images/{n}.png')
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        # Saving the array in a text file
        np.save(f'./pokeContours/{n}.npy', contours[0])
        list.append(contours[0])
    return list


def getPokeContours():
    list = []
    for n in range(150):
        data = np.load(f'./pokeContours/{n}.npy')
        list.append(data)
    return list


savePokeCountours()
