import cv2
import numpy as np

from contour import get_contours
from details import getPokemonData
from frame_editor import apply_color_convertion
from test import getPokeContours
from trackbar import create_trackbar


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

    pokeDict = getPokemonData()
    pokeContours = getPokeContours()

    while True:
        ret, frame = cap.read()

        # Cuts square in the middle of the screen to only detect contours in there
        width = int(cap.get(3))  # float `width`
        height = int(cap.get(4))  # float `height`
        ROI = frame[int(height * 0.3):int(height * 0.7), int(width * 0.3):int(width * 0.7)]

        colors = frame.copy()
        gray_frame = apply_color_convertion(frame=ROI, color=cv2.COLOR_RGB2GRAY)
        ret1, thresh1 = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY_INV)
        contours = get_contours(frame=thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []

        for c in contours:
            if 30000 < cv2.contourArea(c):
                filtered.append(c)

        if len(filtered) > 0:

            for f in filtered:

                for index in range(len(pokeContours)):
                    if cv2.matchShapes(f, pokeContours[index], cv2.CONTOURS_MATCH_I2, 0) < 0.4:
                        x, y, w, h = cv2.boundingRect(f)
                        text = getPokeData(pokeDict.get(index))
                        for i, line in enumerate(text.split('\n')):
                            y1 = y + i * 50
                            cv2.putText(colors, line, (x + w + 10, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)
                        cv2.drawContours(colors, f, -1, color_green, 20)

                    # else:
                    #     x, y, w, h = cv2.boundingRect(f)
                    #     cv2.rectangle(imGris, (x, y), (x + w, y + h), color_red, 20)
                    #     cv2.putText(imGris, 'Unidentified', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_red, 2)

        cv2.imshow('Tp Final', colors)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


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
