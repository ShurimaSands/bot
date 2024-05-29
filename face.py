import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Inicialización de Pygame y la ventana de OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

def draw_circle(radius, segments, clockwise=True):
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        theta = 2.0 * np.pi * i / segments
        if not clockwise:
            theta = -theta
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        glVertex2f(x, y)
    glEnd()

def draw_face(angle):
    glColor3f(0.0, 1.0, 0.0)
    for i, r in enumerate(np.linspace(0.1, 2.0, 20)):
        draw_circle(r, 50, clockwise=(i % 2 == 0))

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

angle = 0

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    draw_face(angle)
    glPopMatrix()

    angle += 1
    pygame.display.flip()
    pygame.time.wait(10)
