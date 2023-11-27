from object import *
from camera import *
import pygame as pg
from tkinter import *
import copy


class ThreeDimensionalEngine:
    def __init__(self):
        pg.init()
        print("|<======================3D Renderer start======================>|")
        self.ScreenRES = self.WIDTH, self.HEIGHT = 800, 600  # set the size of the screen
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()

        self.objectList = []
        self.create_objects()

        self.font1 = pg.font.SysFont("arial", 18)

        self.viewPortMatrix = np.array([
            [self.WIDTH, 0, 0, self.H_WIDTH],  # the actual rendering size should be twice bigger as the screen size
            [0, -self.HEIGHT, 0, self.H_HEIGHT],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def create_objects(self):
        self.camera = Camera(self, [1, 1, -55],rotationMode="anyAxis")
        cube = Object(self)
        cube.vertices = np.array([[0, 0, 0, 1],
                                  [0, 20, 0, 1],
                                  [20, 20, 0, 1],
                                  [20, 0, 0, 1],
                                  [0, 0, 20, 1],
                                  [0, 20, 20, 1],
                                  [20, 20, 20, 1],
                                  [20, 0, 20, 1]])
        cube.faces = np.array([[0, 1, 2, 3],
                               [4, 5, 6, 7],
                               [0, 4, 5, 1],
                               [2, 3, 7, 6],
                               [1, 2, 6, 5],
                               [0, 3, 7, 4]])
        cube.worldCoordinate = np.array([0, 5, 0])
        cube.color_faces = [list(np.random.choice(range(256), size=3)) for face in cube.faces]

        floor = Face(self)

        tank = self.get_object_from_file('resources/t_34_obj.obj')
        tank.translate([0, 0, -8])
        tank.color_faces = [list(np.random.choice(range(256), size=3)) for face in tank.faces]

        sphere = self.get_object_from_file('resources/sphere.obj')
        sphere.translate([-25, -25, -25])
        sphere.scale(7)

        #self.objectList.append(sphere)
        self.objectList.append(floor)
        self.objectList.append(tank)
        #self.objectList.append(cube)

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])

        return Object(self, vertex, faces)

    def drawGen1(self, object: Object, drawPoints=False):
        """self.print_text( 0, 280, u"direction matrix: "+str(self.camera.cameraDirectionMatrix[0]))
        self.print_text(0, 330, u"direction matrix: " + str(self.camera.cameraDirectionMatrix[1]))
        self.print_text(0, 380, u"direction matrix: " + str(self.camera.cameraDirectionMatrix[2]))
        self.print_text(0, 430, u"direction matrix: " + str(self.camera.cameraDirectionMatrix[3]))

        self.print_text(0, 480, u"position matrix: " + str(self.camera.position))"""
        pointsPositionSave = []

        # print("point:", point)
        worldSpaceCoordinate = object.vertices + np.r_[object.worldCoordinate, np.array([0])]
        # print("worldSpaceCoordinate:",worldSpaceCoordinate)
        cameraSpaceCoordinate = self.camera.getProjectionMatrix_Slow() @ worldSpaceCoordinate.T
        # print("cameraSpaceCoordinate:", cameraSpaceCoordinate)

        # Optimization possible
        X = cameraSpaceCoordinate[0] * self.camera.NEAR / cameraSpaceCoordinate[2]
        Y = -cameraSpaceCoordinate[1] * self.camera.NEAR / cameraSpaceCoordinate[2]
        x = (self.WIDTH - 1) * (X / (self.camera.RIGHT * 2) + 0.5)
        y = (self.HEIGHT - 1) * (Y / (self.camera.TOP * 2) + 0.5)
        pointsPositionSave = list(zip(x, y))
        # pointsPositionSave.append((x,y))

        # print(normalMatrix)

        for i in range(len(x)):
            pg.draw.circle(self.screen, (255, 255, 255), [x[i], y[i]], 3)

        for face in object.faces:
            pg.draw.lines(self.screen, (255, 255, 100), True, [pointsPositionSave[i] for i in face], 1)
        # print("---")

    def drawGen2(self, object: Object, drawPoints=False, drawLines=True):

        # print("point:", point)
        worldSpaceCoordinate = object.vertices + np.r_[object.worldCoordinate, np.array([0])]
        # print("worldSpaceCoordinate:",worldSpaceCoordinate.T)

        cameraSpaceCoordinate = self.camera.getCamMatrix() @ worldSpaceCoordinate.T
        # print("cameraSpaceCoordinate:", cameraSpaceCoordinate)

        normalSpace = self.camera.PerMatrix @ cameraSpaceCoordinate
        normalSpace /= normalSpace[3]

        mask = np.all(np.abs(normalSpace) <= 1, axis=0)
        # print("normalSpace:",normalSpace)

        screenMatrix = self.viewPortMatrix @ normalSpace
        # print("screenMatrix:", screenMatrix)
        if drawPoints:
            for i in range(len(normalSpace[0])):
                if mask[i]:
                    pg.draw.circle(self.screen, (255, 255, 255),
                                   [screenMatrix[0][i] / screenMatrix[3][i], screenMatrix[1][i] / screenMatrix[3][i]],
                                   3)

        for face in object.faces:
            if np.all([mask[i] for i in face]):
                pg.draw.lines(self.screen, (255, 255, 100), True,
                              [(screenMatrix[0][i] / screenMatrix[3][i], screenMatrix[1][i] / screenMatrix[3][i]) for i
                               in face], 1)

    def drawGen3(self, drawPoints=False, drawLines=False, drawFace=True):

        for object in self.objectList:

            worldCoordinates = (object.vertices + np.r_[
                object.worldCoordinate, np.array([0])]).T  # coordinates in the world system

            normalSpaceMatrix = self.camera.PerMatrix @ self.camera.getCamMatrix()  # a matrix that convert the coordinates into a [-1,1]^3 cube

            normalSpace = normalSpaceMatrix @ worldCoordinates  # caculating the matrix above an above and then applying them to all coordinates is faster than calculating them one by one

            normalSpace /= normalSpace[
                3]  # devide the normalized matrix by its w to extract real coordinates from Homogeneous coordinate

            mask = np.all(np.abs(normalSpace) <= 1,
                          axis=0)  # mark all coordinates that is out of the [-1,1]^3 cube, which means they should not be rendered

            screenMatrix = self.viewPortMatrix @ normalSpace  # convert the x,y coordinates to the screen coordinate system

            if drawFace:
                faceBuffer = []
                for faceIndex in range(
                        len(object.faces)):  # use the average depth of a face to decide the order of rendering
                    if np.all([mask[i] for i in
                               object.faces[faceIndex]]):  # only if the all the verticies are inside the view cube
                        averageDepth = 0
                        for point in object.faces[faceIndex]:
                            averageDepth += screenMatrix[2][point]
                        averageDepth /= len(object.faces[faceIndex])

                        faceBuffer.append((faceIndex, averageDepth))

                faceBuffer.sort(key=lambda x: x[1], reverse=True)

                for faceIndex, depth in faceBuffer:  # draw faces
                    # print(worldCoordinate[2][object.faces[faceIndex][0]])
                    # print(object.color_faces[faceIndex])
                    pg.draw.polygon(self.screen, object.color_faces[faceIndex],
                                    [(screenMatrix[0][pointIndex], screenMatrix[1][pointIndex]) for pointIndex in
                                     object.faces[faceIndex]])

            if drawLines:
                for face in object.faces:
                    if np.all([mask[i] for i in face]):
                        pg.draw.aalines(self.screen, (255, 255, 100), True,
                                      [(screenMatrix[0][i], screenMatrix[1][i]) for i in face], 1)

            if drawPoints:
                for i in range(len(normalSpace[0])):
                    if mask[i]:
                        pg.draw.circle(self.screen, (255, 255, 255),
                                       [screenMatrix[0][i], screenMatrix[1][i]], 3)

    def print_text(self, x, y, text, color=(255, 255, 255)):
        """print text to screen"""
        img_text = self.font1.render(text, True, color)
        self.screen.blit(img_text, (x, y))

    def run(self):
        """the main draw loop"""
        while True:

            self.screen.fill((pg.Color("green")))
            pg.draw.rect(self.screen, pg.Color("black"), ((0, 0), (self.WIDTH, self.HEIGHT)))

            """for object in self.objectList:
                self.drawGen1(object)"""

            """for object in self.objectList:
                self.drawGen2(object)"""

            self.drawGen3()

            self.camera.control()  # get input from keyboard and do transform to the direction matrix of the camera
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))  # show FPS on caption
            pg.display.flip()
            self.clock.tick(self.FPS)  # set maximum FPS


if __name__ == '__main__':
    app = ThreeDimensionalEngine()
    app.run()
