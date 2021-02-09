import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from random import randint, random

counter = 0

# Line class for simple lines created using opengl lines.
class SimpleLine:
    def __init__(self, x, y, thickness, zoom, z=0):  # z parameter just for some fun probably never will be used
        self.verticies = []
        self.thickness = thickness
        self.verticies.append((x, y, z))
        self.verticies.append((x + thickness * zoom, y, z))
        self.color = (random(), random(), random())

    #  TODO: thickness isnt really needed on each vertex this is 4 testing
    def add_vertex(self, x, y, thickness, z=0):
        self.verticies.append((x, y, z))

    def draw(self):
        verts = self.verticies
        # Set thickness to the specified one
        glLineWidth(self.thickness)
        for i in range(len(verts) - 1):
            glBegin(GL_LINES)
            glColor3fv(self.color)
            glVertex3f(verts[i][0], verts[i][1], verts[i][2])
            glVertex3f(verts[i + 1][0], verts[i + 1][1], verts[i + 1][2])
            glEnd()


def calculate_zoom(zoom, d, translation, zoom_shift, near, far):
    # TODO Zoom that follows the mouse
    # Reproject the view with the zoom applied
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # remove the zoom shift from translation for zoom calculations
    translation = (translation[0] + zoom_shift[0], translation[1] + zoom_shift[1], translation[2])
    dx = d[0] - d[0] * zoom
    dy = d[1] - d[1] * zoom
    zoom_shift = dx / 2, dy / 2
    x1 = dx / 2 - translation[0]
    x2 = (d[0] - dx / 2) - translation[0]
    y1 = (d[1] - dy / 2) - translation[1]
    y2 = dy / 2 - translation[1]
    # Zooming adds a translation factor that has to be taken into account in future calculations
    # Add new zoom shift back in to the translation after zoom calculations
    translation = (translation[0] - zoom_shift[0], translation[1] - zoom_shift[1], translation[2])
    glOrtho(x1, x2, y1, y2, near, far)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    return translation, zoom_shift


def main():
    lines = []  # list of lines to render
    pygame.init()
    d = (1280, 720)  # Display diemensions
    zoom = 1
    zoom_factor = 0.1
    translation = (0, 0, 0)
    zoom_shift = (0, 0)
    x1, x2, y1, y2, near, far = 0, d[0], d[1], 0, -1, 1  # Data for orthographic projection

    pygame.display.set_caption("Blackboard OpenGL")
    # Setup pygame for opengl
    pygame.display.set_mode(d, DOUBLEBUF | OPENGL)
    glOrtho(x1, x2, y1, y2, near, far)
    glTranslatef(0, 0, -1)
    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        diff = pygame.mouse.get_rel()

        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex3f(d[0] / 2 * zoom - 2.5 - translation[0], d[1] / 2 * zoom - translation[1], 0)
        glVertex3f(d[0] / 2 * zoom + 2.5 - translation[0], d[1] / 2 * zoom - translation[1], 0)
        glEnd()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # if mouse button down add line
                if event.button == 1:
                    lines.append(
                        SimpleLine(pos[0] * zoom - translation[0], pos[1] * zoom - translation[1], 5, zoom))
            elif event.type == pygame.MOUSEMOTION and pressed[0]:
                lines[-1].add_vertex(pos[0] * zoom - translation[0], pos[1] * zoom - translation[1], 5)

            if event.type == pygame.MOUSEMOTION and pressed[2]:
                translation = (translation[0] + (diff[0] * zoom), translation[1] + (diff[1] * zoom), translation[2])
                glTranslate(diff[0] * zoom, diff[1] * zoom, 0)

            # Zoom
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom -= zoom * zoom_factor
                else:
                    zoom += zoom * zoom_factor
                # Apply the zoom
                translation, zoom_shift = calculate_zoom(zoom, d, translation, zoom_shift, near, far)

        for line in lines:
            line.draw()

        pygame.display.flip()
        pygame.time.wait(16)


main()
