import cv2
import numpy as np
from details import getPokemonData


def cart2pol(x, y):
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)
    return theta, rho


def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y


def rotate_contour(cnt, angle):
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    cnt_norm = cnt - [cx, cy]

    coordinates = cnt_norm[:, 0, :]
    xs, ys = coordinates[:, 0], coordinates[:, 1]
    thetas, rhos = cart2pol(xs, ys)

    thetas = np.rad2deg(thetas)
    thetas = (thetas + angle) % 360
    thetas = np.deg2rad(thetas)

    xs, ys = pol2cart(thetas, rhos)

    cnt_norm[:, 0, 0] = xs
    cnt_norm[:, 0, 1] = ys

    cnt_rotated = cnt_norm + [cx, cy]
    cnt_rotated = cnt_rotated.astype(np.int32)

    return cnt_rotated


def scale_contour(cnt, scale):
    M = cv2.moments(cnt)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def generateWithFor(number, name):
    color_green = (0, 255, 0)
    cap = cv2.VideoCapture(0)
    contour = np.load(f'./pokeContours/{number}.npy')
    for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        cont = scale_contour(contour, x / 10)
        for a in [1, 10, 20, 50, 120, 130, 150, 180, 200, 240, 260, 280, 300, 310, 350]:
            print(x)
            print(a)
            final_cont = rotate_contour(cont, a)
            np.save(f'./pokeShapes/{name}/{number}-{x}-{a}.npy', final_cont)
            ret, frame = cap.read()
            cv2.drawContours(frame, final_cont, -1, color_green, 1)
            cv2.imshow('test', frame)
            cv2.waitKey()


def main():
    # pokeDict = getPokemonData()
    generateWithFor(79, 'Slowpoke')


main()
