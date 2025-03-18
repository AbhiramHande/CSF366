# Module to control the motors of the robot
import keyboard
import Jetson.GPIO as GPIO
from time import sleep

# Define GPIO pins
in1_motor_hor = 24          #Physical pin 18
in2_motor_hor = 23          #Physical pin 16
in3_motor_hor = 26          #Physical pin 37
in4_motor_hor = 19          #Physical pin 35

in1_motor_ver = 9           #Physical pin 21
in2_motor_ver = 10          #Physical pin 19
in3_motor_ver = 27          #Physical pin 13
in4_motor_ver = 22          #Physical pin 15

ena_horizontal = 13 # Connected to 13 and - Physical pin 33
ena_vertical = 12 # Connected to 11 and 17 - Physical pin 32

# Define arrays
motors = [in1_motor_hor, in2_motor_hor, in3_motor_hor, in4_motor_hor,
          in1_motor_ver, in2_motor_ver, in3_motor_ver, in4_motor_ver]
enable_motors = None

def setup():
    global enable_motors
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    for pin in motors:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    GPIO.setup(ena_horizontal, GPIO.OUT)
    GPIO.setup(ena_vertical, GPIO.OUT)
    pwm_hor = GPIO.PWM(ena_horizontal, 1000)
    pwm_ver = GPIO.PWM(ena_vertical, 1000)
    enable_motors = [pwm_hor, pwm_ver]

    for pwm in enable_motors:
        pwm.start(0)

# Functions that will help control the direction of movement
def set_pins_high_except(inactive_pins=None):
    if inactive_pins is None:
        inactive_pins = set()

    for pin in motors:
        if pin not in inactive_pins:
            GPIO.output(pin, GPIO.HIGH) 

def set_pins_low_except(active_pins=None):
    if active_pins is None:
        active_pins = set()

    for pin in motors:
        if pin not in active_pins:
            GPIO.output(pin, GPIO.LOW) 

def stop_move():
    # or set_pins_low_except()
    for pin in motors:
        GPIO.output(pin, GPIO.LOW)

def horizontal_move():
    set_pins_low_except([in1_motor_hor, in3_motor_hor])
    GPIO.output(in1_motor_hor, GPIO.HIGH)
    GPIO.output(in3_motor_hor, GPIO.HIGH)

def horizontal_rmove():
    set_pins_low_except([in2_motor_hor, in4_motor_hor])
    GPIO.output(in2_motor_hor, GPIO.HIGH)
    GPIO.output(in4_motor_hor, GPIO.HIGH)

def vertical_move():
    set_pins_low_except([in1_motor_ver, in3_motor_ver])
    GPIO.output(in1_motor_ver, GPIO.HIGH)
    GPIO.output(in3_motor_ver, GPIO.HIGH)

def vertical_rmove():
    set_pins_low_except([in2_motor_ver, in4_motor_ver])
    GPIO.output(in2_motor_ver, GPIO.HIGH)
    GPIO.output(in4_motor_ver, GPIO.HIGH)

# Angle is defined in degrees for simplicity
def rotate_clockwise(angle=None):
    active_pins = [in1_motor_hor, in4_motor_hor, in1_motor_ver, in4_motor_ver]
    set_pins_low_except(active_pins)
    for pin in active_pins:
        GPIO.output(pin, GPIO.HIGH)
    
    if angle is None:
        return
    else:
        sleep(0.1) #TODO Calculate and change accordingly
        stop_move
        return
        

def rotate_anticlockwise(angle=None):
    active_pins = [in2_motor_hor, in3_motor_hor, in2_motor_ver, in3_motor_ver]
    set_pins_low_except(active_pins)
    for pin in active_pins:
        GPIO.output(pin, GPIO.HIGH)
    
    if angle is None:
        return
    else:
        sleep(0.1) #TODO Calculate and change accordingly
        stop_move
        return

# Functions that will help control the speed the of motor
def speed_custom(value):
    if value > 100 or value < 0:
        print("Error: Duty Cycle must be between 0 and 100")
        return

    if enable_motors is None or not enable_motors:
        print("Error: Motors are not initialized properly")
        return
    
    for pwm in enable_motors:
        pwm.ChangeDutyCycle(value)

def speed_slow():
    speed_custom(50)

def speed_med():
    speed_custom(75)

def speed_high():
    speed_custom(90)

def speed_full():
    speed_custom(100)

# Main to test the movements if directly executed
if __name__ == "__main__":
    setup()
    stop_move()
    speed_full()

    try:
        while True:
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                horizontal_move()
            elif keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                horizontal_rmove()
            elif keyboard.is_pressed('a') or keyboard.is_pressed('left'):
                vertical_move()
            elif keyboard.is_pressed('d') or keyboard.is_pressed('right'):
                vertical_rmove()
            elif keyboard.is_pressed('q'):
                print("Exiting...")
                break
            elif keyboard.is_pressed('r'):
                rotate_clockwise()
            elif keyboard.is_pressed('p'):
                rotate_anticlockwise()
            else:
                stop_move()

            sleep(0.2)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        stop_move()
        speed_custom(0)
        GPIO.cleanup()