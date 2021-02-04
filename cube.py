import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# The "nodes" and their location in space
verticies = (
    (1, -1, -1),  # 0
    (1, 1, -1),  # 1
    (-1, 1, -1),  # 2
    (-1, -1, -1),  # 3
    (1, -1, 1),  # 4
    (1, 1, 1),  # 5
    (-1, -1, 1),  # 6
    (-1, 1, 1)  # 7
)

# edge is connection between two nodes. You use the node index in the list and the other that it conects to
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
)
colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 1),
    (1, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 1),
    (1, 1, 1),
)
zoom_ratio = 9.5

def Cube():
    # Set color, Draw faces
    glBegin(GL_QUADS)

    for surface in surfaces:
        c = 0
        for vertex in surface:
            c += 1
            glColor3fv(colors[c])
            glVertex3fv(verticies[vertex])
    glEnd()

    # Encapsulate opengl code in these markers, you also specify what you are drawing
    glLineWidth(3)
    glBegin(GL_LINES)
    # Set color
    # Draw connections between verticies. You specify verticies in glVertex3fv and do GL_Lines - draw lines in
    # between each
    glColor3fv((0.2, 0.8, 0.2))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    # create pygame display, tell it using opengl
    pygame.init()
    display = (1280, 720)
    pygame.display.set_caption("Blackboard OpenGL")
    # Double buffer - two buffers and use opengl 4 em
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # setting camera parameters fov, aspect ratio (width/ height), clipping plane (how far away to render)
    glOrtho(-display[0]/200, display[0]/200, -display[1]/200, display[1]/200, -1, 10)
    glOrtho(-5, 5, -5, 5, -1, 10)
    print("Bruh")
    # x, y, z
    glTranslatef(0.0, 0.0, -5)
    # glRotatef(25, 2, 2, 0)
    while True:
        # Gets the position data
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        coord = [[c for c in r] for r in x]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Key Events
            if event.type == pygame.KEYDOWN:
                if event.key == ord("a"):
                    glTranslatef(-1, 0, 0)
                if event.key == ord("d"):
                    glTranslatef(1, 0, 0)
                if event.key == ord("w"):
                    glTranslatef(0, 1, 0)
                if event.key == ord("s"):
                    glTranslatef(0, -1, 0)
                if event.key == ord("f"):
                    glOrtho(-10/zoom_ratio, 10/zoom_ratio, -10/zoom_ratio, 10/zoom_ratio, -1, 10)
                if event.key == ord("r"):
                    glOrtho(-zoom_ratio/10, zoom_ratio/10, -zoom_ratio/10, zoom_ratio/10, -1, 10)
                if event.key == pygame.K_UP:
                    glRotatef(20, 1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(20, -1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(20, 0, 1, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(20, 0, -1, 0)
        # clear screen, what to clear, this should clear everything
        # glRotatef(3, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
