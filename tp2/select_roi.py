import cv2


def select_roi():
    image = cv2.imread('screenshot.png')
    show_image = True
    while show_image:
        cv2.imshow('screenshot', image)
        key = cv2.waitKey()
        if key == ord("s"):
            box = cv2.selectROI("Frame", image, fromCenter=False,
                                showCrosshair=True)
            print(box)
        if key == ord("q"):
            show_image = False
