import numpy as np


def rotation_matrix(degree, axis):
    radian = degree * np.pi / 180.0

    magnitude = np.sqrt(np.dot(axis, axis))
    x, y, z = axis / magnitude if magnitude != 0 else axis

    return np.array([[
        np.cos(radian) + (x ** 2 * (1 - np.cos(radian))),
        x * y * (1 - np.cos(radian)) - z * np.sin(radian),
        x * z * (1 - np.cos(radian)) + y * np.sin(radian),
        0,
    ], [
        y * x * (1 - np.cos(radian)) + z * np.sin(radian),
        np.cos(radian) + y ** 2 * (1 - np.cos(radian)),
        y * z * (1 - np.cos(radian)) - x * np.sin(radian),
        0,
    ], [
        z * x * (1 - np.cos(radian)) - y * np.sin(radian),
        z * y * (1 - np.cos(radian)) + x * np.sin(radian),
        np.cos(radian) + z ** 2 * (1 - np.cos(radian)),
        0,
    ], [0, 0, 0, 1]], dtype=np.float32)
