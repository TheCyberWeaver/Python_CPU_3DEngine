import pygame as pg
from Functions import *




class Object:
    def __init__(self, render, vertices='', faces=''):

        self.name=""
        self.engine = render
        self.vertices = np.array([np.array(v) for v in vertices])
        #self.faces = np.array([np.array(face) for face in faces])
        self.faces = faces

        """self.vertices = np.array([[0, 0, 0, 1],
                              [0, 5, 0, 1],
                              [5, 5, 0, 1],
                              [5, 0, 0, 1],
                              [0, 0, 5, 1],
                              [0, 5, 5, 1],
                              [5, 5, 5, 1],
                              [5, 0, 5, 1]])
        self.faces = np.array([[0,1,2,3],
                              [4,5,6,7],
                              [0,4,5,1],
                               [2,3,7,6],
                               [1,2,6,5],
                               [0,3,7,4]])"""

        #self.translate([0.0001, 0.0001, 0.0001])

        self.worldCoordinate=np.array([0,0,0])

        self.font = pg.font.SysFont('Arial', 30, bold=True)
        #self.color_faces = [(pg.Color('orange'), face) for face in self.faces]

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)


class Axes(Object):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'

class Face(Object):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = []
        n = 10
        for i in range(-n, n):
            for j in range(-n, n):
                self.vertices.append([i * 5, 0, j * 5, 1])

        self.faces = []
        for i in range(0, n * 2 - 1):
            for j in range(0, n * 2 - 1):
                self.faces.append([i * 20 + j, i * 20 + j + 1, (i + 1) * 20 + j + 1, (i + 1) * 20 + j])
        self.worldCoordinate = np.array([0, 0, 0])