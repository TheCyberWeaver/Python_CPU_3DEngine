import pygame as pg
from Functions import *


class Camera:
    def __init__(self, render, position,rotationMode="anyAxis"):
        self.render = render
        self.rotationMode=rotationMode
        self.position = np.array([*position, 1.0])
        """self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])"""
        # right(x+),up(y+),forward(z+)
        self.cameraDirectionMatrix = np.array([[1, 0, 0, 0],
                                               [0, 1, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])

        self.h_fov = np.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.moving_speed = 0.5
        self.rotation_speed = 0.015

        # OLD
        self.NEAR = 0.1
        self.FAR = 100
        self.RIGHT = np.tan(self.h_fov / 2)
        self.LEFT = -self.RIGHT
        self.TOP = np.tan(self.v_fov / 2)
        self.BOTTOM = -self.TOP

        NEAR = 0.5
        FAR = 1000
        RIGHT = np.tan(self.h_fov / 2)
        LEFT = -RIGHT
        TOP = np.tan(self.v_fov / 2)
        BOTTOM = -TOP

        self.projectionMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        self.angleVertical = 0
        self.angleHorizontal = 0

        self.PerMatrix = np.array([
            [2 * NEAR / (RIGHT - LEFT), 0, 0, 0],
            [0, 2 * NEAR / (TOP - BOTTOM), 0, 0],
            [0, 0, (NEAR + FAR) / (FAR - NEAR), -(2 * NEAR * FAR) / (FAR - NEAR)],
            [0, 0, 1, 0]
        ])

        self.I = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.cameraDirectionMatrix[:, 0] * self.moving_speed
        if key[pg.K_d]:
            self.position += self.cameraDirectionMatrix[:, 0] * self.moving_speed
        if key[pg.K_w]:
            self.position += self.cameraDirectionMatrix[:, 2] * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.cameraDirectionMatrix[:, 2] * self.moving_speed
        if key[pg.K_q]:
            self.position -= self.cameraDirectionMatrix[:, 1] * self.moving_speed
        if key[pg.K_e]:
            self.position += self.cameraDirectionMatrix[:, 1] * self.moving_speed

        if key[pg.K_LEFT]:
            self.cameraHorizontal(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.cameraHorizontal(self.rotation_speed)
        if key[pg.K_UP]:
            self.cameraVertical(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.cameraVertical(self.rotation_speed)
        if key[pg.K_o]:
            self.cameraExtraZrotate(-self.rotation_speed)
        if key[pg.K_p]:
            self.cameraExtraZrotate(self.rotation_speed)

    def cameraHorizontal(self, angle):
        self.angleHorizontal += angle
        if self.rotationMode=="anyAxis":
            Nx = self.cameraDirectionMatrix[0][1]
            Ny = self.cameraDirectionMatrix[1][1]
            Nz = self.cameraDirectionMatrix[2][1]
            C = 1 - np.cos(angle)
            rotationMatrix = np.array([
                [Nx * Nx * C + np.cos(angle), Nx * Ny * C - Nz * np.sin(angle), Nx * Nz * C + Ny * np.sin(angle), 0],
                [Nx * Ny * C + Nz * np.sin(angle), Ny * Ny * C + np.cos(angle), Ny * Nz * C - Nx * np.sin(angle), 0],
                [Nx * Nz * C - Ny * np.sin(angle), Ny * Nz * C + Nx * np.sin(angle), Nz * Nz * C + np.cos(angle), 0],
                [0,0,0,1]
            ])
            self.cameraDirectionMatrix = rotationMatrix @ self.cameraDirectionMatrix
        elif self.rotationMode=="euler":
            self.cameraDirectionMatrix = rotate_y(-angle) @ self.cameraDirectionMatrix
        elif self.rotationMode=="fromOrigin":
            self.cameraDirectionMatrix = rotate_y(-self.angleHorizontal) @ self.I
    def cameraVertical(self, angle):
        self.angleVertical += angle

        if self.rotationMode == "anyAxis":
            Nx = self.cameraDirectionMatrix[0][0]
            Ny = self.cameraDirectionMatrix[1][0]
            Nz = self.cameraDirectionMatrix[2][0]
            C = 1 - np.cos(angle)
            rotationMatrix = np.array([
                [Nx * Nx * C + np.cos(angle), Nx * Ny * C - Nz * np.sin(angle), Nx * Nz * C + Ny * np.sin(angle), 0],
                [Nx * Ny * C + Nz * np.sin(angle), Ny * Ny * C + np.cos(angle), Ny * Nz * C - Nx * np.sin(angle), 0],
                [Nx * Nz * C - Ny * np.sin(angle), Ny * Nz * C + Nx * np.sin(angle), Nz * Nz * C + np.cos(angle), 0],
                [0, 0, 0, 1]
            ])
            self.cameraDirectionMatrix = rotationMatrix @ self.cameraDirectionMatrix
        elif self.rotationMode == "euler":
            self.cameraDirectionMatrix = rotate_x(-angle) @ self.cameraDirectionMatrix
        elif self.rotationMode == "fromOrigin":
            self.cameraDirectionMatrix = rotate_x(-self.angleVertical) @ self.I
    def cameraExtraZrotate(self,angle):

        if self.rotationMode == "anyAxis":
            Nx = self.cameraDirectionMatrix[0][2]
            Ny = self.cameraDirectionMatrix[1][2]
            Nz = self.cameraDirectionMatrix[2][2]
            C = 1 - np.cos(angle)
            rotationMatrix = np.array([
                [Nx * Nx * C + np.cos(angle), Nx * Ny * C - Nz * np.sin(angle), Nx * Nz * C + Ny * np.sin(angle), 0],
                [Nx * Ny * C + Nz * np.sin(angle), Ny * Ny * C + np.cos(angle), Ny * Nz * C - Nx * np.sin(angle), 0],
                [Nx * Nz * C - Ny * np.sin(angle), Ny * Nz * C + Nx * np.sin(angle), Nz * Nz * C + np.cos(angle), 0],
                [0, 0, 0, 1]
            ])
            self.cameraDirectionMatrix = rotationMatrix @ self.cameraDirectionMatrix

    def getProjectionMatrix_Slow(self):
        # print(self.cameraDirectionMatrix,self.position)
        matrix = np.c_[self.cameraDirectionMatrix[:3, :3].T, (- self.cameraDirectionMatrix.T @ self.position)[:-1]]
        matrix = np.r_[matrix, np.array([[0, 0, 0, 1]])]
        # print(matrix)
        return matrix

    def getCamMatrix(self):
        positionMatrix = np.array([
            [1, 0, 0, -self.position[0]],
            [0, 1, 0, -self.position[1]],
            [0, 0, 1, -self.position[2]],
            [0, 0, 0, 1]
        ])

        return self.cameraDirectionMatrix.T @ positionMatrix
