import cv2
import numpy as np

from contour import get_contours, get_poke_contours
from frame_editor import apply_color_convertion, denoise
from details import getPokemonData
from test import getPokeContours
from trackbar import create_trackbar, get_trackbar_value


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
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)
        ret1, thresh1 = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY_INV)
        contours = get_contours(frame=thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []

        for c in contours:
            if 30000 < cv2.contourArea(c):
                filtered.append(c)

        imGris = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2RGB)

        if len(filtered) > 0:

            for f in filtered:

                for index in range(len(pokeContours)):
                    if cv2.matchShapes(f, pokeContours[index], cv2.CONTOURS_MATCH_I2, 0) < 0.4:
                        x, y, w, h = cv2.boundingRect(f)
                        cv2.putText(imGris, pokeDict.get(index).name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)
                        cv2.drawContours(imGris, f, -1, color_green, 20)

                    # else:
                    #     x, y, w, h = cv2.boundingRect(f)
                    #     cv2.rectangle(imGris, (x, y), (x + w, y + h), color_red, 20)
                    #     cv2.putText(imGris, 'Unidentified', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_red, 2)

        cv2.imshow('Tp Final', imGris)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


main()
