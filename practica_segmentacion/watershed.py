import numpy as np
import cv2 as cv

img = cv.imread('../static/images/water_coins.jpeg')

selectedNumber = 1

labels = np.zeros((img.shape[0], img.shape[1]), np.int32)

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
        labels[y][x] = selectedNumber
        cv.imshow('img', img)


def watershed():
    global selectedNumber
    global labels
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # convierte a gris
    # _, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    cv.imshow("img", img)  # muestra la imagen guardada

    while True:

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

        # cv.setMouseCallback('img', draw_circles)  # permite clickear
        cv.imshow('img', gray)  # muestra la imagen gris

        if cv.waitKey() == ord(' '):  # espera un input que sea igual a ESPACIO
            fg = np.uint8(np.random.random((2, 2, 3)) * 255)
            dst = cv.integral(fg)
            ret, thresh = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)  # transforma la imagen gris a binario
            cv.imshow('thresh', thresh)
            cv.waitKey()
            _, labels = cv.connectedComponents(image=thresh)
            labels = labels + 1
            newLabels = labels.astype(np.int32)
            water = cv.watershed(dst, newLabels)
            # img[markers == 0] = [255, 0, 0]
            cv.imshow('water', water)
            if cv.waitKey() == ord('m'):
                break


watershed()
