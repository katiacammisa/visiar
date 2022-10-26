import math

import cv2
import numpy as np

from contour import get_contours
from frame_editor import apply_color_convertion
from label_converters import int_to_label


def load_and_test(model):
    cap = cv2.VideoCapture(0)  # Replace 0 with droidcam app link (http://IP:port/video)
    while True:
        ret, frame = cap.read()
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)
        ret1, thresh1 = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY_INV)
        contours = get_contours(frame=thresh1, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []

        for c in contours:
            if 30000 < cv2.contourArea(c):
                filtered.append(c)

        if len(filtered) > 0:
            for f in filtered:
                moments = cv2.moments(f)
                huMoments = cv2.HuMoments(moments)
                for i in range(0, 7):
                    huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(
                        abs(huMoments[i]))
                sample = np.array([huMoments], dtype=np.float32)  # numpy
                testResponse = model.predict(sample)[1]  # Predice la clase de cada file
                print(testResponse)
                # image_with_text = cv2.putText(frame, int_to_label(testResponse), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                #                               (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Tp Final', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
