#A simple program to test whether the GPIO pins of Jetson and the L298N Motor Cards work as expected
import subprocess
import keyboard
import Jetson.GPIO as GPIO
from time import sleep

# Display GPIO pin status
# try:
#     result = subprocess.run(['jetson-gpio', 'info'], capture_output=True, text=True)
#     print(result.stdout)
# except FileNotFoundError:
#     print("'jetson-gpio' command not found, skipping pin status check.")

# Define GPIO pins
in_motor_bkd_1 = 24
in_motor_bkd_2 = 23
in_motor_bkd_3 = 26
in_motor_bkd_4 = 19

in_motor_fwd_1 = 9
in_motor_fwd_2 = 10
in_motor_fwd_3 = 27
in_motor_fwd_4 = 22

ena_a_high = 13
ena_b_high = 25
ena_a_low = 11
ena_b_low = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup Motors for Vertical Movement
for pin in [in_motor_fwd_1, in_motor_fwd_2, in_motor_fwd_3, in_motor_fwd_4, ena_a_low, ena_b_low]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pwm_1 = GPIO.PWM(ena_a_low, 1000)
pwm_2 = GPIO.PWM(ena_b_low, 1000)

# Setup Motors for Horizontal Movement
for pin in [in_motor_bkd_1, in_motor_bkd_2, in_motor_bkd_3, in_motor_bkd_4, ena_a_high, ena_b_high]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pwm_3 = GPIO.PWM(ena_a_high, 1000)
pwm_4 = GPIO.PWM(ena_b_high, 1000)

def stop_move():
    print("Halting...")
    for pin in [in_motor_fwd_1, in_motor_fwd_2, in_motor_fwd_3, in_motor_fwd_4, 
                in_motor_bkd_1, in_motor_bkd_2, in_motor_bkd_3, in_motor_bkd_4]:
        GPIO.output(pin, GPIO.LOW)

def forward_move():
    GPIO.output(in_motor_fwd_1, GPIO.HIGH)
    GPIO.output(in_motor_fwd_2, GPIO.LOW)
    GPIO.output(in_motor_fwd_3, GPIO.HIGH)
    GPIO.output(in_motor_fwd_4, GPIO.LOW)
    stop_move_except([in_motor_fwd_1, in_motor_fwd_3])

def backward_move():
    GPIO.output(in_motor_fwd_1, GPIO.LOW)
    GPIO.output(in_motor_fwd_2, GPIO.HIGH)
    GPIO.output(in_motor_fwd_3, GPIO.LOW)
    GPIO.output(in_motor_fwd_4, GPIO.HIGH)
    stop_move_except([in_motor_fwd_2, in_motor_fwd_4])

def side_fwd_move():
    GPIO.output(in_motor_bkd_1, GPIO.HIGH)
    GPIO.output(in_motor_bkd_2, GPIO.LOW)
    GPIO.output(in_motor_bkd_3, GPIO.HIGH)
    GPIO.output(in_motor_bkd_4, GPIO.LOW)
    stop_move_except([in_motor_bkd_1, in_motor_bkd_3])

def side_bkd_move():
    GPIO.output(in_motor_bkd_1, GPIO.LOW)
    GPIO.output(in_motor_bkd_2, GPIO.HIGH)
    GPIO.output(in_motor_bkd_3, GPIO.LOW)
    GPIO.output(in_motor_bkd_4, GPIO.HIGH)
    stop_move_except([in_motor_bkd_2, in_motor_bkd_4])

def stop_move_except(active_pins):
    for pin in [in_motor_fwd_1, in_motor_fwd_2, in_motor_fwd_3, in_motor_fwd_4, 
                in_motor_bkd_1, in_motor_bkd_2, in_motor_bkd_3, in_motor_bkd_4]:
        GPIO.output(pin, GPIO.LOW)

def speed_med():
    for pwm in [pwm_1, pwm_2, pwm_3, pwm_4]:
        pwm.ChangeDutyCycle(75)

def speed_full():
    for pwm in [pwm_1, pwm_2, pwm_3, pwm_4]:
        pwm.ChangeDutyCycle(100)

def start_setup():
    for pwm in [pwm_1, pwm_2, pwm_3, pwm_4]:
        pwm.start(100)
    for pin in [ena_a_low, ena_b_low, ena_a_high, ena_b_high]:
        GPIO.output(pin, GPIO.HIGH)

def main():
    start_setup()
    speed_full()
    try:
        while True:
            if keyboard.is_pressed('w'):
                forward_move()
            elif keyboard.is_pressed('s'):
                backward_move()
            elif keyboard.is_pressed('a'):
                side_fwd_move()
            elif keyboard.is_pressed('d'):
                side_bkd_move()
            elif keyboard.is_pressed('q'):
                print("Exiting...")
                break
            else:
                stop_move()

            sleep(0.2)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        stop_move()
        GPIO.cleanup()

main()
