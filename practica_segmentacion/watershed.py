import numpy as np
import cv2 as cv

img = cv.imread('../static/images/messi.jpg')

img_copy = img.copy()

selectedNumber = 1

labels = np.zeros((img.shape[0], img.shape[1]), np.uint8)

labels_copy = labels.copy()

colorMap = {
    1: (255, 255, 255),
    2: (255, 0, 0),
    3: (0, 255, 0),
    4: (0, 0, 255),
    5: (0, 0, 0),
}


def draw_circles(event, x, y, _1, _2):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img_copy, (x, y), 7, colorMap.get(selectedNumber), -1)
        cv.circle(labels, (x, y), 7, colorMap.get(selectedNumber), -1)
        cv.circle(labels_copy, (x, y), 7, colorMap.get(selectedNumber), -1)


def watershed():
    global selectedNumber
    global labels
    global labels_copy
    global img

    vc = cv.VideoCapture(0)
    _, frame = vc.read()
    frame_copy = frame.copy()

    cv.imshow("img", frame_copy)  # muestra la copia de la imagen guardada
    map = cv.applyColorMap(labels_copy, cv.COLORMAP_JET)
    cv.imshow("labels", map)  # muestra la imagen guardada

    cv.setMouseCallback('img', draw_circles)

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

        if cv.waitKey() == ord(' '):  # espera un input que sea igual a ESPACIO
            print(labels)
            print(np.int32(labels))
            frame_copy2 = frame.copy()
            water = cv.watershed(frame_copy2, np.int32(labels))

            frame_copy2[water == -1] = [0, 0, 255]
            for n in range(1, 6):
                frame_copy2[water == n] = colorMap[n]

            print(water)
            cv.imshow('result', frame_copy2)

            if cv.waitKey() == ord('q'):
                break

        vc.release()


watershed()
