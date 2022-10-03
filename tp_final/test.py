import cv2 as cv

from trackbar import get_trackbar_value, create_trackbar

def main():    
    image = cv.imread('./images/1.png')
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    ret1, thresh1 = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # contours = [cnt1, cnt2, cnt3]
    

    window_name = 'Tp Final'
    trackbar_name = 'Threshold'
    cv.namedWindow(window_name)
    create_trackbar(trackbar_name, window_name, 0, 100)
    for cont in contours:
        trackbar_value = get_trackbar_value(trackbar_name=trackbar_name, window_name=window_name)

        cv.drawContours(image, cont, -1, (0, 0, 255), 3)
        cv.imshow(window_name, image)

        cv.waitKey()

main()