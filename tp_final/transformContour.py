import cv2
import numpy as np


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


def main():
    contour = np.load(f'./pokeContours/0.npy')
    cnt_scaled = scale_contour(contour, 0.3)
    cnt_rotated = rotate_contour(contour, 60)
    cnt_scaled1 = scale_contour(contour, 0.6)
    cnt_rotated1 = rotate_contour(contour, 80)
    cnt_scaled2 = scale_contour(contour, 0.9)
    cnt_rotated2 = rotate_contour(contour, 20)

    contour1 = np.load(f'./pokeContours/1.npy')
    cnt_scaled3 = scale_contour(contour1, 0.3)
    cnt_rotated3 = rotate_contour(contour1, 60)
    cnt_scaled4 = scale_contour(contour1, 0.6)
    cnt_rotated4 = rotate_contour(contour1, 80)
    cnt_scaled5 = scale_contour(contour1, 0.9)
    cnt_rotated5 = rotate_contour(contour1, 20)

    np.save(f'./pokeShapes/Bulbasor/0-0.npy', contour)
    np.save(f'./pokeShapes/Bulbasor/0-1.npy', cnt_scaled)
    np.save(f'./pokeShapes/Bulbasor/0-2.npy', cnt_rotated)
    np.save(f'./pokeShapes/Bulbasor/0-3.npy', cnt_scaled1)
    np.save(f'./pokeShapes/Bulbasor/0-4.npy', cnt_rotated1)
    np.save(f'./pokeShapes/Bulbasor/0-5.npy', cnt_scaled2)
    np.save(f'./pokeShapes/Bulbasor/0-6.npy', cnt_rotated2)

    np.save(f'./pokeShapes/Ivysaur/1-0.npy', contour1)
    np.save(f'./pokeShapes/Ivysaur/1-1.npy', cnt_scaled3)
    np.save(f'./pokeShapes/Ivysaur/1-2.npy', cnt_rotated3)
    np.save(f'./pokeShapes/Ivysaur/1-3.npy', cnt_scaled4)
    np.save(f'./pokeShapes/Ivysaur/1-4.npy', cnt_rotated4)
    np.save(f'./pokeShapes/Ivysaur/1-5.npy', cnt_scaled5)
    np.save(f'./pokeShapes/Ivysaur/1-6.npy', cnt_rotated5)


main()
