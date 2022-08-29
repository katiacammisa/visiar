import cv2 as cv


def moments():
    heart = cv.imread('../static/images/heart.jpeg')
    gray1 = cv.cvtColor(heart, cv.COLOR_RGB2GRAY)
    ret1, thresh1 = cv.threshold(gray1, 127, 255, cv.THRESH_BINARY)
    contours1, hierarchy = cv.findContours(thresh1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    cnt1 = contours1[0]
    cv.drawContours(heart, [cnt1], -1, (0, 0, 255), 2)
    cv.imshow("heart", heart)
    momentsVariable = cv.moments(cnt1)
    cv.waitKey(0)
    huMoments = cv.HuMoments(momentsVariable)
    print(huMoments)


moments()
