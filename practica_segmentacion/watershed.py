import numpy as np
import cv2 as cv

img = cv.imread('../static/images/water_coins.jpeg')

selectedNumber = 1

labels = np.zeros((img.shape[1], img.shape[0]), np.float64)

colorMap = {
    1: (255, 255, 255),
    2: (255, 0, 0),
    3: (0, 255, 0),
    4: (0, 0, 255),
    5: (0, 0, 0),
}


def draw_circles(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 7, colorMap.get(selectedNumber), -1)
        labels[x][y] = selectedNumber
        cv.imshow('img', img)


def watershed():
    global selectedNumber
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    cv.imshow("img", img)

    if cv.waitKey() == ord('1'):
        selectedNumber = 1
    elif cv.waitKey() == ord('2'):
        selectedNumber = 2
    elif cv.waitKey() == ord('3'):
        selectedNumber = 3
    elif cv.waitKey() == ord('4'):
        selectedNumber = 4
    elif cv.waitKey() == ord('5'):
        selectedNumber = 5

    # noise removal
    # kernel = np.ones((3, 3), np.uint8)
    # opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    # closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=2)

    cv.setMouseCallback('img', draw_circles)
    cv.imshow('img', img)

    # markers = cv.watershed(img, markers)
    #
    # print(img)
    # print(markers)
    #
    # img[markers == -1] = [255, 0, 0]

    cv.imshow("img", img)

    cv.waitKey()


watershed()
