import numpy as np


def toHomogeneousCoordinate(matrix):
    matrix=np.c_[matrix,[0,0,0]]
    matrix=np.r_[matrix,np.array([[0, 0, 0, 1]])]
    return matrix


def translate(vector):
    tx, ty, tz = vector
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1]
    ])


def rotate_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(a), np.sin(a), 0],
        [0, -np.sin(a), np.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_y(a):
    return np.array([
        [np.cos(a), 0, -np.sin(a), 0],
        [0, 1, 0, 0],
        [np.sin(a), 0, np.cos(a), 0],
        [0, 0, 0, 1]
    ])


def rotate_z(a):
    return np.array([
        [np.cos(a), np.sin(a), 0, 0],
        [-np.sin(a), np.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(n):
    return np.array([
        [n, 0, 0, 0],
        [0, n, 0, 0],
        [0, 0, n, 0],
        [0, 0, 0, 1]
    ])


