import cv2

from select_roi import select_roi
from grabcut import grabcut


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow('screenshot', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.imwrite('screenshot.png', frame)
            # select_roi()
            grabcut()

    cap.release()


main()
