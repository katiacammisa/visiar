import cv2
from joblib import load
import numpy as np


from contour import get_contours
from frame_editor import apply_color_convertion, denoise
from moment import get_hu_moments
from trackbar import create_trackbar, get_trackbar_value


def main():
    window_name = 'Tp Detección'
    trackbar_name = 'Threshold'
    trackbar_name2 = 'Noise filter'
    trackbar_name3 = 'Size filter'
    slider_max = 255
    cv2.namedWindow(window_name)
    color_green = (0, 255, 0)
    cap = cv2.VideoCapture("http://172.20.10.5:4747/video")
    create_trackbar(trackbar_name, window_name, 100, slider_max)
    create_trackbar(trackbar_name2, window_name, 0, 50)
    create_trackbar(trackbar_name3, window_name, 60000, 100000)
    saved_contours = []
    classifier = load('training.joblib')

    while True:
        ret, frame = cap.read()
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)
        trackbar_val = get_trackbar_value(trackbar_name=trackbar_name, window_name=window_name)
        ret10, adapt_frame = cv2.threshold(gray_frame, trackbar_val, slider_max, cv2.THRESH_BINARY)
        # adapt_frame = adaptive_threshold(frame=gray_frame, slider_max=slider_max,
        #                                  adaptative=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                  binary=cv2.THRESH_BINARY,
        #                                  trackbar_value=trackbar_val)
        trackbar_val2 = get_trackbar_value(trackbar_name=trackbar_name2, window_name=window_name)
        frame_denoised = denoise(frame=adapt_frame, method=cv2.MORPH_ELLIPSE, radius=trackbar_val2)
        trackbar_val3 = get_trackbar_value(trackbar_name=trackbar_name3, window_name=window_name)

        contours = get_contours(frame=frame_denoised, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []
        for c in contours:
            if 5000 < cv2.contourArea(c) < trackbar_val3:
                filtered.append(c)

        for f in filtered:
            imGris = cv2.cvtColor(frame_denoised, cv2.COLOR_GRAY2RGB)

            moments_view = get_hu_moments(f)

            predicted = classifier.predict([moments_view])
            cv2.drawContours(imGris, f, -1, color_green, 20)
            x, y, w, h = cv2.boundingRect(f)
            text = 'Figura'
            if predicted == 1:
                text = 'Corazon'

            if predicted == 2:
                text = 'Estrella'

            if predicted == 3:
                text = 'Cuadrado'

            cv2.putText(imGris, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)

            cv2.imshow('Tp Detección', imGris)
            if cv2.waitKey(1) & 0xFF == ord('k'):
                if f is not None:
                    saved_contours.append(f)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


main()
