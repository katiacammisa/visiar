import cv2

from contour import get_contours, get_biggest_contour, compare_contours
from frame_editor import apply_color_convertion, adaptive_threshold, denoise, draw_contours
from trackbar import create_trackbar, get_trackbar_value


def main():

    window_name = 'Window'
    trackbar_name = 'Threshold'
    trackbar_name2 = 'Noise filter'
    slider_max = 151
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(0)
    biggest_contour = None
    color_white = (255, 255, 255)
    color_red = (0, 0, 255)
    create_trackbar(trackbar_name, window_name, slider_max)
    create_trackbar(trackbar_name2, window_name, 50)
    # saved_hu_moments = load_hu_moments(file_name="hu_moments.txt")
    saved_contours = []

    while True:
        ret, frame = cap.read()
        gray_frame = apply_color_convertion(frame=frame, color=cv2.COLOR_RGB2GRAY)
        trackbar_val = get_trackbar_value(trackbar_name=trackbar_name, window_name=window_name)
        adapt_frame = adaptive_threshold(frame=gray_frame, slider_max=slider_max,
                                         adaptative=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         binary=cv2.THRESH_BINARY,
                                         trackbar_value=trackbar_val)
        trackbar_val2 = get_trackbar_value(trackbar_name=trackbar_name2, window_name=window_name)
        frame_denoised = denoise(frame=adapt_frame, method=cv2.MORPH_ELLIPSE, radius=trackbar_val2)
        # terminamos el 3

        alphabet = cv2.imread('../static/images/image.jpeg')
        gray2 = cv2.cvtColor(alphabet, cv2.COLOR_RGB2GRAY)
        ret2, thresh2 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY)
        contoursblah, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt1 = contoursblah[0]

        anteojos = cv2.imread('../static/images/anteojos.jpeg')
        gray2anteojos = cv2.cvtColor(anteojos, cv2.COLOR_RGB2GRAY)
        ret2anteojos, thresh2anteojos = cv2.threshold(gray2anteojos, 127, 255, cv2.THRESH_BINARY)
        contoursblahAnteojos, hierarchyAnteojos = cv2.findContours(thresh2anteojos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt1anteojos = contoursblahAnteojos[0]

        contours = get_contours(frame=frame_denoised, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            biggest_contour = get_biggest_contour(contours=contours)
            # hu_moments = get_hu_moments(contour=biggest_contour)
            # if compare_contours(contour_to_compare=biggest_contour, saved_contours=saved_contours, max_diff=1):
            #     draw_contours(frame=frame_denoised, contours=biggest_contour, color=color_white, thickness=20)
            # draw_contours(frame=frame_denoised, contours=biggest_contour, color=color_white, thickness=20)

        # print(biggest_contour)
        #
        # for contour in contours:
        #     moments_alphabet = cv2.moments(contour)
        #     huMoments_alphabet = cv2.HuMoments(moments_alphabet)

        imGris = cv2.cvtColor(frame_denoised, cv2.COLOR_GRAY2RGB)

        if cv2.matchShapes(biggest_contour, cnt1, cv2.CONTOURS_MATCH_I2, 0) < 0.4:
            print("MATCHIE CON CELU")
            cv2.drawContours(imGris, biggest_contour, -1, color_white, 20)
            cv2.imshow("contornos", alphabet)
        else:
            print("MORI CON CELU")

        if cv2.matchShapes(biggest_contour, cnt1anteojos, cv2.CONTOURS_MATCH_I2, 0) < 0.4:
            print("MATCHIE CON ANTEOJOS")
            cv2.drawContours(imGris, biggest_contour, -1, color_red, 20)
            cv2.imshow("contornos", anteojos)
        else:
            print("MORI CON ANTEOJOS")

        cv2.imshow('Window', imGris)
        if cv2.waitKey(1) & 0xFF == ord('k'):
            if biggest_contour is not None:
                # save_moment(hu_moments=hu_moments, file_name="hu_moments.txt")
                saved_contours.append(biggest_contour)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


main()
