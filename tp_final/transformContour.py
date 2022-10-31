import os

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
    contour = np.load(f'./pokeContours/{number}.npy')
    for x in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        cont = scale_contour(contour, x / 10)
        for a in [1, 10, 20, 50, 120, 130, 150, 180, 200, 240, 260, 280, 300, 310, 350]:
            final_cont = rotate_contour(cont, a)
            np.save(f'./pokeShapes/{name}/{number}-{x}-{a}.npy', final_cont)


def main():
    pokeDict = getPokemonData()
    brokenIndexes = [99, 100, 52, 61, 149, 148, 145, 144, 143, 141, 135, 130, 129, 126, 125, 124, 123, 121, 118, 117,
                     112, 111, 109, 108, 98, 92, 91, 84, 83, 77, 76, 51, 48, 40, 37, 33, 25, 21, 5, 4, 54, 55, 58, 62,
                     66, 67, 73, 74]
    for i in range(150):
        if i in brokenIndexes: continue
        os.makedirs('./pokeShapes/' + pokeDict.get(i).name)
        generateWithFor(pokeDict.get(i).number, pokeDict.get(i).name)


main()
