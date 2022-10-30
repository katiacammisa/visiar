import cv2


def get_contours(frame, mode, method):
    contours, hierarchy = cv2.findContours(frame, mode, method)
    return contours


def get_biggest_contour(contours):
    max_cnt = contours[0]
    second_max = contours[1]
    for cnt in contours:
        if cv2.contourArea(cnt) > cv2.contourArea(max_cnt):
            second_max = max_cnt
            max_cnt = cnt
    print(len(contours))
    return contours[113]


def compare_contours(contour_to_compare, saved_contours, max_diff):
    for contour in saved_contours:
        if cv2.matchShapes(contour_to_compare, contour, cv2.CONTOURS_MATCH_I2, 0) < max_diff:
            return True
    return False

def get_poke_contours():
    contours = []
    for n in range(1, 152):
        img = cv2.imread(f'./images/{n}.jpeg')
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret2, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contoursPoke, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours.append(contoursPoke[0])
    return contours
