import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import multiprocessing

def draw_sphere(radius, lats, longs):
    for i in range(0, lats + 1):
        lat0 = np.pi * (-0.5 + float(i - 1) / lats)
        z0 = radius * np.sin(lat0)
        zr0 = radius * np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i) / lats)
        z1 = radius * np.sin(lat1)
        zr1 = radius * np.cos(lat1)

        glBegin(GL_LINE_STRIP)
        for j in range(0, longs + 1):
            lng = 2 * np.pi * float(j - 1) / longs
            x = np.cos(lng)
            y = np.sin(lng)

            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_face_3d(angle, talking):
    if talking.value:
        glColor3f(0.0, 0.0, 1.0)  # Blue color when talking
    else:
        glColor3f(0.0, 1.0, 0.0)  # Green color otherwise

    draw_sphere(2.0, 50, 50)

def face_animation(talking):
    pygame.init()
    display = (640, 480)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glRotatef(45, 1, 1, 0)
    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        draw_face_3d(angle, talking)
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    talking = multiprocessing.Value('i', 0)
    face_animation(talking)
