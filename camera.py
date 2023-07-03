import pygame as pg
from Functions import *


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        """self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])"""
                                            #right(x+),up(y+),forward(z+)
        self.cameraDirectionMatrix = np.array([[1, 0, 0, 0],
                                               [0, 1, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])

        self.h_fov = np.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.moving_speed = 0.5
        self.rotation_speed = 0.015

        #OLD
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


        self.PerMatrix=np.array([
            [2*NEAR/(RIGHT-LEFT),0,0,0],
            [0,2*NEAR/(TOP-BOTTOM),0,0],
            [0,0,(NEAR+FAR)/(FAR-NEAR),-(2*NEAR*FAR)/(FAR-NEAR)],
            [0,0,1,0]
        ])



    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.cameraDirectionMatrix[:,0] * self.moving_speed
        if key[pg.K_d]:
            self.position += self.cameraDirectionMatrix[:,0] * self.moving_speed
        if key[pg.K_w]:
            self.position += self.cameraDirectionMatrix[:,2] * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.cameraDirectionMatrix[:,2] * self.moving_speed
        if key[pg.K_q]:
            self.position -= self.cameraDirectionMatrix[:,1] * self.moving_speed
        if key[pg.K_e]:
            self.position += self.cameraDirectionMatrix[:,1] * self.moving_speed

        if key[pg.K_LEFT]:
            self.cameraHorizontal(self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.cameraHorizontal(-self.rotation_speed)
        if key[pg.K_UP]:
            self.cameraVertical(self.rotation_speed)
        if key[pg.K_DOWN]:
            self.cameraVertical(-self.rotation_speed)

    def cameraHorizontal(self, angle):
        self.angleHorizontal += angle
        self.cameraDirectionMatrix=rotate_y(angle) @ self.cameraDirectionMatrix


    def cameraVertical(self, angle):
        self.angleVertical += angle
        self.cameraDirectionMatrix = rotate_x(angle) @ self.cameraDirectionMatrix


    def getProjectionMatrix_Slow(self):
        #print(self.cameraDirectionMatrix,self.position)
        matrix=np.c_[self.cameraDirectionMatrix[:3,:3].T,(- self.cameraDirectionMatrix.T @ self.position)[:-1]]
        matrix=np.r_[matrix,np.array([[0,0,0,1]])]
        #print(matrix)
        return matrix
    def getCamMatrix(self):
        positionMatrix=np.array([
            [1, 0, 0,-self.position[0]],
            [0, 1, 0, -self.position[1]],
            [0, 0, 1, -self.position[2]],
            [0, 0, 0, 1]
        ])

        return self.cameraDirectionMatrix.T @ positionMatrix
