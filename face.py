import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import multiprocessing

def draw_circle(radius, segments, z=0):
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * np.pi * i / segments
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        glVertex3f(x, y, z)
    glEnd()

def draw_face_3d(angle, talking):
    if talking.value:
        glColor3f(0.0, 0.0, 1.0)  # Blue color when talking
    else:
        glColor3f(0.0, 1.0, 0.0)  # Green color otherwise

    for i, r in enumerate(np.linspace(0.1, 2.0, 20)):
        draw_circle(r, 50, z=i*0.1 if i % 2 == 0 else -i*0.1)

    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-1, 1, 0)
    draw_circle(0.25, 50)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(1, 1, 0)
    draw_circle(0.25, 50)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -1.5, 0)
    draw_circle(1, 50)
    glPopMatrix()

def face_animation(talking):
    pygame.init()
    display = (800, 600)
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
