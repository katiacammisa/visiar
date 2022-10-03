import cv2

from contour import get_contours
from frame_editor import apply_color_convertion, denoise
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
    detected_contours = []
    saved_contours = []



    while True:
        ret, frame = cap.read()
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)  # Hace la imagen gris
        trackbar_val = get_trackbar_value(trackbar_name=trackbar_name, window_name=window_name)
        ret10, adapt_frame = cv2.threshold(gray_frame, trackbar_val, slider_max, cv2.THRESH_BINARY)
        trackbar_val2 = get_trackbar_value(trackbar_name=trackbar_name2, window_name=window_name)
        frame_denoised = denoise(frame=adapt_frame, method=cv2.MORPH_ELLIPSE, radius=trackbar_val2)

        contours = get_contours(frame=frame_denoised, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        filtered = []
        for c in contours:
            if 7000 < cv2.contourArea(c) < 50000:
                filtered.append(c)

        if len(filtered) < 1:
            print("filtered is empty")

        imGris = cv2.cvtColor(frame_denoised, cv2.COLOR_GRAY2RGB)

        if len(filtered) > 0:

            for f in filtered:

                if cv2.waitKey(1) & 0xFF == ord('k'):
                    if f is not None:
                        detected_contours.append(f)

                for n in range(1, 2):
                    img = cv2.imread(f'./images/{n}.png')
                    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    ret2, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                    contoursPoke, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    cv2.drawContours(imGris, contoursPoke[20], -1, color_green, 20)

                for contour in saved_contours:
                    if cv2.matchShapes(f, contour, cv2.CONTOURS_MATCH_I2, 0) < 0.2:
                        x, y, w, h = cv2.boundingRect(f)
                        # cv2.rectangle(imGris, (x, y), (x + w, y + h), color_green, 20)
                        # cv2.putText(imGris, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_green, 2)
                        # cv2.drawContours(imGris, contours, -1, color_green, 20)

                else:
                    x, y, w, h = cv2.boundingRect(f)
                    cv2.rectangle(imGris, (x, y), (x + w, y + h), color_red, 20)
                    cv2.putText(imGris, 'Unidentified', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_red, 2)

        cv2.imshow('Tp Final', imGris)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


main()
