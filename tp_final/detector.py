import cv2
import numpy as np

from contour import get_contours
from details import getPokemonData
from frame_editor import apply_color_convertion
from test import getPokeContours
from trackbar import create_trackbar
import functools


def main():
    window_name = 'Tp Final'
    trackbar_name = 'Threshold'
    trackbar_name2 = 'Noise filter'
    slider_max = 255
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(0)  # Replace 0 with droidcam app link (hhtp://IP:port/video)
    color_red = (0, 0, 255)
    color_green = (0, 255, 0)
    create_trackbar(trackbar_name, window_name, 1, slider_max)
    create_trackbar(trackbar_name2, window_name, 1, 50)
    brokenIndeces = [99, 100, 52, 61, 149, 148, 145, 144, 143, 141, 135, 130, 129, 126, 125, 124, 123, 121, 118, 117,
                     112, 111, 109, 108, 98, 92, 91, 84, 83, 77, 76, 51, 48, 40, 37, 33, 25, 21, 5, 4, 54, 55, 58, 62,
                     66, 67, 73, 74]

    pokeDict = getPokemonData()
    pokeContours = getPokeContours()
    lastMatches = []

    while True:
        ret, frame = cap.read()

        colors = frame.copy()
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)
        ret1, thresh1 = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY_INV)
        contours = get_contours(frame=thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []

        for c in contours:
            if 30000 < cv2.contourArea(c):
                filtered.append(c)

        if len(filtered) > 0:
            f = min(filtered, key=lambda cont: cv2.contourArea(cont))
            matchedShapes = []

            for index in range(len(pokeContours)):
                if index in brokenIndeces:
                    continue
                matchedShapes.append((cv2.matchShapes(f, pokeContours[index], cv2.CONTOURS_MATCH_I2, 0), index))

            # minimumMatchedShape is a tuple with the match value and the index it was detected in (pokemon number)
            minimumMatchedShape = functools.reduce(lambda a, b: a if a[0] < b[0] else b, matchedShapes)
            if minimumMatchedShape[0] < 0.3:
                lastMatches.append(minimumMatchedShape[1])
                matchedPokemonNumber = most_repeated(lastMatches)
                x, y, w, h = cv2.boundingRect(f)
                draw_text(color_green, colors, f, matchedPokemonNumber, pokeDict, w, x, y)

        cv2.imshow('Tp Final', colors)
        print(len(lastMatches))
        if len(lastMatches) == 60:
            lastMatches.pop(0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


def most_repeated(lst):
    return max(set(lst), key=lst.count)


def draw_text(color_green, colors, f, pokemonNumber, pokeDict, w, x, y):
    # Add text to pokemon
    text = getPokeData(pokeDict.get(pokemonNumber))
    for i, line in enumerate(text.split('\n')):
        y1 = y + i * 50
        cv2.putText(colors, line, (x + w + 10, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)
    cv2.drawContours(colors, f, -1, color_green, 20)


def getPokeData(poke):
    if poke.number < 10:
        number = str('00' + str(poke.number))
    elif 10 <= poke.number < 100:
        number = str('0' + str(poke.number))
    else:
        number = str(poke.number)
    name = poke.name
    attack = poke.attack
    baseExp = poke.baseExp
    type = poke.type
    category = poke.category
    weight1 = np.char.split(poke.weight, "(").tolist()[1]
    weight2 = np.char.split(weight1, ")").tolist()[0]
    height1 = np.char.split(poke.height, "(").tolist()[1]
    height2 = np.char.split(height1, ")").tolist()[0]
    abilities = poke.abilities
    return "Number: " + number + \
           "\nName: " + name + \
           "\nAttack: " + str(attack) + \
           "\nBase Experience: " + str(baseExp) + \
           "\nType: " + str(type) + \
           "\nCategory: " + str(category) + \
           "\nWeight: " + str(weight2) + \
           "\nHeight: " + str(height2) + \
           "\nAbilities: " + abilities


main()
