import cv2 as cv
import numpy as np

from details import getPokemonData
from scrapper import saveImageFromUrl


def savePokeCountours():
    pokeDict = getPokemonData()
    list = []
    brokenIndeces = [99, 100, 52, 61, 149, 148, 145, 144, 143, 141, 135, 130, 129, 126, 125, 124, 123, 121, 118, 117,
                     112, 111, 109, 108, 98, 92, 91, 84, 83, 77, 76, 51, 48, 40, 37, 33, 25, 21, 5, 4, 54, 55, 58, 62,
                     66, 67, 73, 74]
    for n in range(150):
        if n in brokenIndeces: continue
        url = pokeDict.get(n).image
        saveImageFromUrl(n, url)
        image = cv.imread(f'./images/{n}.png')
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

        # Saving the array in a text file
        np.save(f'./pokeContours/{n}.npy', contours[0])
        list.append(pokeDict.get(n).name)

    with open('pokemonNames.txt', 'w') as file:
        for name in list:
            file.write("%s\n" % name)

    return list


def getPokeContours():
    list = []
    for n in range(150):
        data = np.load(f'./pokeContours/{n}.npy')
        list.append(data)
    return list


savePokeCountours()
