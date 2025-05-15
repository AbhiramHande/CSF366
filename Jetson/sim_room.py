import sys
import time
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from sim_robot import Robot

window_width, window_height = 800, 800
room_corners = []
delta_time = 1/24

robot = Robot()
robot.set_speed(25)

pulse_radius = 10.0
pulse_increasing = True
target_point = None

def load_room(filename="room.txt"):
    global room_corners
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split())
            room_corners.append((x, y))

def draw_grid():
    glColor3f(0.3, 0.3, 0.3)
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

def draw_robot():
    glColor3f(1.0, 0.0, 0.0)

    size = 20
    center = robot.position
    dir_f = robot.dir_facing
    dir_l = robot.dir_left
    tip = [center[0] + dir_f[0] * size, center[1] + dir_f[1] * size]
    left = [center[0] + dir_l[0] * size / 2, center[1] + dir_l[1] * size / 2]
    right = [center[0] - dir_l[0] * size / 2, center[1] - dir_l[1] * size / 2]

    glBegin(GL_TRIANGLES)
    glVertex2f(*tip)
    glVertex2f(*left)
    glVertex2f(*right)
    glEnd()

def draw_pulsating_circle():
    if not target_point:
        return

    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    segments = 50
    for i in range(segments):
        theta = 2 * math.pi * i / segments
        x = target_point[0] + pulse_radius * math.cos(theta)
        y = target_point[1] + pulse_radius * math.sin(theta)
        glVertex2f(x, y)
    glEnd()

def draw_path():
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(3)
    glBegin(GL_POINTS)
    for x, y in robot.path:
        glVertex2f(x, y)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()
    draw_room()
    draw_path()
    draw_robot()
    draw_pulsating_circle()
    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-600, 600, -600, 600)
    glMatrixMode(GL_MODELVIEW)

def update(value):
    global target_point, pulse_radius, pulse_increasing

    robot.move_horizontal(delta_time)
    if len(robot.path) % 120 == 0:
        robot.rotate_clockwise(45)

    # Find nearest wall point along facing direction
    target_point = robot.get_nearest_wall_coord(robot.dir_facing, room_corners)

    # Update pulse
    if pulse_increasing:
        pulse_radius += 0.5
        if pulse_radius > 20: pulse_increasing = False
    else:
        pulse_radius -= 0.5
        if pulse_radius < 10: pulse_increasing = True

    glutPostRedisplay()
    glutTimerFunc(int(delta_time * 1000), update, 0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"2D Robot Simulation")

    load_room()
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
