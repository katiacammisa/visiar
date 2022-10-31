import cv2 as cv
import numpy as np


def savePokeCountours():
    list = []
    brokenIndeces = [99, 100, 52, 61, 149, 148, 145, 144, 143, 141, 135, 130, 129, 126, 125, 124, 123, 121, 118, 117,
                     112, 111, 109, 108, 98, 92, 91, 84, 83, 77, 76, 51, 48, 40, 37, 33, 25, 21, 5, 4, 54, 55, 58, 62,
                     66, 67, 73, 74]
    for n in range(1, 150):
        if n-1 in brokenIndeces: continue
        image = cv.imread(f'./images/{n - 1}.png')
        gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        cv.drawContours(image, contours[0], -1, (0, 255, 0), 5)
        # Saving the array in a text file
        np.save(f'./pokeContours/{n}.npy', contours[0])
        # list.append(pokeDict.get(n).name)

    # with open('pokemonNames.txt', 'w') as file:
    #     for name in list:
    #         file.write("%s\n" % name)

    # return list


def getPokeContours():
    list = []
    for n in range(150):
        data = np.load(f'./pokeContours/{n}.npy')
        list.append(data)
    return list


savePokeCountours()
