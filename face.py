import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import multiprocessing
import time

def draw_sphere(radius, slices, stacks):
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        
        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j) / slices
            x = np.cos(lng)
            y = np.sin(lng)
            
            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
        glEnd()

def draw_ear(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.3, 0.5, 0.1)
    draw_sphere(1.0, 20, 20)
    glPopMatrix()

def draw_face_3d(talking, mouth_open, mouth_shape):
    # Draw face sphere
    glColor3f(0.0, 1.0, 0.0)  # Green color
    glPushMatrix()
    draw_sphere(2.0, 50, 50)
    glPopMatrix()

    # Draw ears
    glColor3f(0.0, 1.0, 0.0)
    draw_ear(-1.5, 0.5, 0)
    draw_ear(1.5, 0.5, 0)

    # Draw eyes
    glColor3f(1.0, 1.0, 1.0)  # White color for eyes
    glPushMatrix()
    glTranslatef(-0.6, 0.6, 1.8)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.6, 0.6, 1.8)
    draw_sphere(0.2, 20, 20)
    glPopMatrix()

    # Draw pupils
    glColor3f(0.0, 0.0, 0.0)  # Black color for pupils
    glPushMatrix()
    glTranslatef(-0.6, 0.6, 2.0)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.6, 0.6, 2.0)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    # Draw mouth
    glColor3f(0.0, 0.0, 0.0)  # Black color for mouth
    glPushMatrix()
    glTranslatef(0.0, -0.6, 1.9)
    glBegin(GL_POLYGON)
    if mouth_shape == 'wide':
        for i in range(180):
            angle = i * np.pi / 180
            glVertex2f(np.cos(angle) * 0.8, np.sin(angle) * 0.6)
    elif mouth_shape == 'narrow':
        for i in range(180):
            angle = i * np.pi / 180
            glVertex2f(np.cos(angle) * 0.5, np.sin(angle) * 0.4)
    else:
        for i in range(180):
            angle = i * np.pi / 180
            glVertex2f(np.cos(angle) * 0.8, np.sin(angle) * 0.4)
    glEnd()
    glPopMatrix()

def face_animation(talking, queue):
    pygame.init()
    display = (640, 480)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    angle = 0
    mouth_shape = 'closed'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if not queue.empty():
            letter = queue.get()
            if letter in 'AEIOUaeiou':
                mouth_shape = 'wide'
            elif letter in 'BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz':
                mouth_shape = 'narrow'
            else:
                mouth_shape = 'closed'

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        draw_face_3d(talking, talking.value, mouth_shape)
        glPopMatrix()

        angle += 1
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    talking = multiprocessing.Value('i', 0)
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=face_animation, args=(talking, queue))
    p.start()

    # Ejemplo de uso de la cola para enviar letras a la animación de la cara
    while True:
        text = input("Ingrese texto para el bot: ")
        for letter in text:
            queue.put(letter)
            time.sleep(0.1)  # Simula el tiempo de pronunciación de cada letra

    p.terminate()
