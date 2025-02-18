import Jetson.GPIO as GPIO
from time import sleep

import Jetson.GPIO as GPIO
from time import sleep

# Define GPIO pins for sensors and motors
LEFT_SENSOR_PIN = 17
RIGHT_SENSOR_PIN = 18
MOTOR_LEFT = 22
MOTOR_RIGHT = 23

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([LEFT_SENSOR_PIN, RIGHT_SENSOR_PIN], GPIO.IN)
GPIO.setup([MOTOR_LEFT, MOTOR_RIGHT], GPIO.OUT)

def rotate_left():
    """Rotates robot left until a wall is found."""
    GPIO.output(MOTOR_LEFT, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT, GPIO.HIGH)

def move_forward():
    """Moves robot forward."""
    GPIO.output(MOTOR_LEFT, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT, GPIO.HIGH)

def stop():
    """Stops all movement."""
    GPIO.output(MOTOR_LEFT, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT, GPIO.LOW)

def find_wall():
    """Finds the closest wall and moves towards it."""
    while GPIO.input(LEFT_SENSOR_PIN) == 0 and GPIO.input(RIGHT_SENSOR_PIN) == 0:
        rotate_left()
        sleep(0.1)
    stop()
    move_forward()
    sleep(1)  # Adjust time to stop at an appropriate distance
    stop()

def stick_to_wall():
    """Keeps following the wall at a fixed distance."""
    while True:
        left_sensor = GPIO.input(LEFT_SENSOR_PIN)
        right_sensor = GPIO.input(RIGHT_SENSOR_PIN)

        if left_sensor == 1:  # Too close to wall
            rotate_left()
        elif right_sensor == 1:  # Too far from wall
            move_forward()
        else:
            stop()

        sleep(0.1)

if __name__ == "__main__":
    find_wall()
    stick_to_wall()
