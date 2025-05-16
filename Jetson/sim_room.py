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
robot.set_speed(50)

MAX_DISTANCE = 400
MIN_DISTANCE = 50

state = 2
pulse_radius = 10.0
pulse_increasing = True
target_point = None
forward_dist = float('inf')
left_dist = float('inf')
extra_dist = 0
extra_dir = None

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
    global pulse_radius, pulse_increasing, target_point, state, forward_dist, left_dist, extra_dist, extra_dir

    def distance_fwd():
        point = robot.get_forward_wall(room_corners)
        if not point:
            return float('inf'), None
        dx = point[0] - robot.position[0]
        dy = point[1] - robot.position[1]
        return math.hypot(dx, dy), point
    
    def distance_left():
        point = robot.get_side_wall(room_corners)
        if not point:
            return float('inf'), None
        dx = point[0] - robot.position[0]
        dy = point[1] - robot.position[1]
        return math.hypot(dx, dy), point

    # Pulsating circle update
    if pulse_increasing:
        pulse_radius += 0.5
        if pulse_radius > 20: pulse_increasing = False
    else:
        pulse_radius -= 0.5
        if pulse_radius < 10: pulse_increasing = True

    # Get directions
    dir_f = robot.dir_facing
    dir_l = [-dir_f[1], dir_f[0]]  # 90° anticlockwise from front

    if state == 2:
        forward_dist, nearest_f = distance_fwd()
        left_dist, nearest_l = distance_left()
        if forward_dist < MAX_DISTANCE:
            state = 5
        elif left_dist < MAX_DISTANCE:
            state = 1
        else:
            state = 4  # default to 4a
        target_point = nearest_f if forward_dist < MAX_DISTANCE else None

    elif state == 1:
        robot.rotate_clockwise(90)
        state = 5

    elif state == 4:
        robot.move_horizontal(delta_time)
        state = 2

    elif state == 5:
        robot.move_horizontal(delta_time)
        forward_dist, nearest_f = distance_fwd()
        left_dist, nearest_l = distance_left()
        if forward_dist < MIN_DISTANCE:
            state = 8
        target_point = nearest_f if forward_dist < MAX_DISTANCE else None

    elif state == 8:
        robot.rotate_clockwise(90)
        state = 9

    elif state == 9:
        robot.move_horizontal(delta_time)
        forward_dist, nearest_f = distance_fwd()
        left_dist, nearest_l = distance_left()
        if forward_dist < MIN_DISTANCE:
            state = 8
        else:
            state = 12
        target_point = nearest_f if forward_dist < MAX_DISTANCE else None

    elif state == 12:
        if left_dist > 2 * MIN_DISTANCE:
            state = 13
        else:
            state = 9

    elif state == 13:
        extra_dist = MIN_DISTANCE
        extra_dir = "fwd"
        state = 14
    
    elif state == 14:
        if extra_dir == "fwd" and extra_dist > 0:
            robot.move_horizontal(delta_time)
            extra_dist -= robot.speed * delta_time
        elif extra_dir == "fwd":
            extra_dir = "side"
            extra_dist = MIN_DISTANCE + 5
        elif extra_dir == "side" and extra_dist > 0:
            robot.move_vertical(delta_time)
            extra_dist -= robot.speed * delta_time
        else:
            robot.rotate_anticlockwise(90)
            state = 9

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
