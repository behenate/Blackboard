import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class LinePart:
    def __init__(self,x,y,z,vector,width):
        p = [vector[0], -vector[1]] # Perpendicular vector to the provided one
        v1 = (x - (width * p[0] / 2), y - (width * p[1] / 2), z)
        v2 = (x + (width * p[0] / 2), y + (width * p[1] / 2), z)
        self.verticies = (v1, v2)


class Line:
    def __init__(self, x, y):
        self.o_x = x
        self.o_y = y
        self.parts = []
        self.parts.append(LinePart(x,y,0,[1,1], 50))


line = Line(50, 50)
line.parts.append(LinePart(100, 100, 0, [1,1], 50))
for part in line.parts:
    print(part.verticies)

def main():
    pygame.init()
    d = (1280, 720) # Display diemensions
    pygame.display.set_caption("Blackboard OpenGL")
    # Setup pygame for opengl
    pygame.display.set_mode(d, DOUBLEBUF | OPENGL)
    glOrtho(0, d[0], 0, d[1], -1, 10)
    glTranslatef(0, 0, -100)
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pygame.display.flip()
        pygame.time.wait(10)
