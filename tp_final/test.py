import cv2 as cv
import pandas as pd

from scrapper import getFromUrl
from trackbar import get_trackbar_value, create_trackbar
from details import getPokemonData

def main():
    pokeDict = getPokemonData()
    n = 2
    image = pokeDict.get(n).image
    getFromUrl(n,image)
    image2 = cv.imread(f'./images/{n}.png')
    gray = cv.cvtColor(image2, cv.COLOR_RGB2GRAY)
    ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY_INV)
    contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    cv.drawContours(image2, contours, -1, (0, 0, 255), 20)
    cv.imshow("blah", image2)
    cv.waitKey()
    # contours = [cnt1, cnt2, cnt3]
    

    window_name = 'Tp Final'
    trackbar_name = 'Threshold'
    cv.namedWindow(window_name)
    create_trackbar(trackbar_name, window_name, 0, 100)
    counter = 0
    for cont in contours:
        trackbar_value = get_trackbar_value(trackbar_name=trackbar_name, window_name=window_name)

        cv.drawContours(gray,cont, -1, (0, 0, 255), 3)
        # cv.drawContours(gray, contours[0], -1, (0, 0, 255), 3)
        cv.imshow(window_name, gray)
        print(counter)
        counter = counter+1

        cv.waitKey()

main()