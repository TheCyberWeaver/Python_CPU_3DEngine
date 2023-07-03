import pygame as pg
import numpy as np
pg.init()
screen = pg.display.set_mode((1200,720))
while True:
    [exit() for i in pg.event.get() if i.type == pg.QUIT]

    screen.fill((pg.Color("green")))
    pg.draw.rect(screen, pg.Color("blue"), ((0, 0), (800, 450)))
    #pg.drawGen2.circle(screen,(255,255,255),[100,100],10)

    vertices = np.array([[0, 0, 0, 1],
                          [0, 5, 0, 1],
                          [5, 5, 0, 1],
                          [5, 0, 0, 1],
                          [0, 0, 5, 1],
                          [0, 5, 5, 1],
                          [5, 5, 5, 1],
                          [5, 0, 5, 1]])
    projectionMatrix=np.array([
        [-1,0,0,-5],
        [0,1,0,-6],
        [0,0,-1,-55],
        [0,0,0,1]
    ])
    M=(projectionMatrix @ vertices.T).T
    N = 1
    for i in M:
        X=i[0]*N/i[2]
        Y=i[1]*N/i[2]
        x=(800-1)*(X/1+0.5)
        y=(450-1)*(Y/0.8+0.5)
        pg.draw.circle(screen, (255, 255, 255), [x, y], 5)


    pg.display.flip()