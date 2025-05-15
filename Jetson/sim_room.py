import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_width, window_height = 800, 800
room_corners = []

def load_room(filename="room.txt"):
    global room_corners
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split())
            room_corners.append((x, y))

def draw_grid():
    glColor3f(0.8, 0.8, 0.8)
    glLineWidth(1)
    glBegin(GL_LINES)
    for i in range(-600, 601, 50):
        # Vertical lines
        glVertex2f(i, -600)
        glVertex2f(i, 600)

        # Horizontal lines
        glVertex2f(-600, i)
        glVertex2f(600, i)
    glEnd()

def draw_room():
    glColor3f(0.2, 0.4, 0.8)
    glLineWidth(3)
    glBegin(GL_LINE_LOOP)
    for x, y in room_corners:
        glVertex2f(x, y)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()
    draw_room()
    glFlush()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-600, 600, -600, 600)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"2D Room Viewer")
    
    load_room()
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    reshape(window_width, window_height)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
