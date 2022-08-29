from joblib import load
import cv2
import numpy as np

from contour import get_contours, get_biggest_contour, compare_contours
from frame_editor import apply_color_convertion, denoise, draw_contours, adaptive_threshold
from trackbar import create_trackbar, get_trackbar_value


def parse(hu_moments_view):
    var = np.array(hu_moments_view)
    return var.flatten()


def main():
    window_name = 'Window'
    trackbar_name = 'Threshold'
    trackbar_name2 = 'Noise filter'
    slider_max = 255
    cv2.namedWindow(window_name)
    color_green = (0, 255, 0)
    cap = cv2.VideoCapture(0)
    biggest_contour = None
    create_trackbar(trackbar_name, window_name, slider_max)
    create_trackbar(trackbar_name2, window_name, 50)
    hu_moments = []
    saved_contours = []

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

        contours = get_contours(frame=frame_denoised, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            biggest_contour = get_biggest_contour(contours=contours)

        imGris = cv2.cvtColor(frame_denoised, cv2.COLOR_GRAY2RGB)

        moments_view = cv2.moments(biggest_contour)
        hu_moments_view = cv2.HuMoments(moments_view)
        hu_moments.append(parse(hu_moments_view))

        # carga el modelo
        classifier = load('training.joblib')

        predicted = classifier.predict(hu_moments)
        cv2.drawContours(imGris, biggest_contour, -1, color_green, 20)
        x, y, w, h = cv2.boundingRect(biggest_contour)
        text = 'Figura'
        if predicted[len(predicted)-1] == 1:
            text = 'Corazon'

        if predicted[len(predicted)-1] == 2:
            text = 'Estrella'

        if predicted[len(predicted)-1] == 3:
            text = 'Cuadrado'

        cv2.putText(imGris, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)
        print(predicted)

        cv2.imshow('Tp Detección', imGris)
        if cv2.waitKey(1) & 0xFF == ord('k'):
            if biggest_contour is not None:
                saved_contours.append(biggest_contour)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


main()
