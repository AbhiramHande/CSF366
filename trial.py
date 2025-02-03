#A simple program to test whether the GPIO pins of RPi and the L298N Motor Cards work as expected
import subprocess
import RPi.GPIO as GPIO
from time import sleep

result = subprocess.run(['raspi-gpio', 'get'], capture_output=True, text=True)
print(result.stdout)   

in_motor_bkd_1 = 24
in_motor_bkd_2 = 23
in_motor_bkd_3 = 13
in_motor_bkd_4 = 19

in_motor_fwd_1 = 15
in_motor_fwd_2 = 18
in_motor_fwd_3 = 27
in_motor_fwd_4 = 22

ena_a_high = 26
ena_b_high = 25
ena_a_low = 14
ena_b_low = 17

GPIO.setmode(GPIO.BCM)

# Setup Motors for Vertical Movement
GPIO.setup(in_motor_fwd_1, GPIO.OUT)
GPIO.setup(in_motor_fwd_2, GPIO.OUT)
GPIO.setup(in_motor_fwd_3, GPIO.OUT)
GPIO.setup(in_motor_fwd_4, GPIO.OUT)
GPIO.setup(ena_a_low, GPIO.OUT)
GPIO.setup(ena_b_low, GPIO.OUT)
GPIO.output(in_motor_fwd_1, GPIO.LOW)
GPIO.output(in_motor_fwd_2, GPIO.LOW)
GPIO.output(in_motor_fwd_3, GPIO.LOW)
GPIO.output(in_motor_fwd_4, GPIO.LOW)
pwm_1 = GPIO.PWM(ena_a_low, 1000)
pwm_2 = GPIO.PWM(ena_b_low, 1000)

# Setup Motors for Horizontal Movement
GPIO.setup(in_motor_bkd_1, GPIO.OUT)
GPIO.setup(in_motor_bkd_2, GPIO.OUT)
GPIO.setup(in_motor_bkd_3, GPIO.OUT)
GPIO.setup(in_motor_bkd_4, GPIO.OUT)
GPIO.setup(ena_a_high, GPIO.OUT)
GPIO.setup(ena_b_high, GPIO.OUT)
GPIO.output(in_motor_bkd_1, GPIO.LOW)
GPIO.output(in_motor_bkd_2, GPIO.LOW)
GPIO.output(in_motor_bkd_3, GPIO.LOW)
GPIO.output(in_motor_bkd_4, GPIO.LOW)
pwm_3 = GPIO.PWM(ena_a_high, 1000)
pwm_4 = GPIO.PWM(ena_b_high, 1000)

def stop_move():
    print("Halting...")
    GPIO.output(in_motor_fwd_1, GPIO.LOW)
    GPIO.output(in_motor_fwd_2, GPIO.LOW)
    GPIO.output(in_motor_fwd_3, GPIO.LOW)
    GPIO.output(in_motor_fwd_4, GPIO.LOW)
    GPIO.output(in_motor_bkd_1, GPIO.LOW)
    GPIO.output(in_motor_bkd_2, GPIO.LOW)
    GPIO.output(in_motor_bkd_3, GPIO.LOW)
    GPIO.output(in_motor_bkd_4, GPIO.LOW)
    
def forward_move():
    GPIO.output(in_motor_fwd_1, GPIO.HIGH)
    GPIO.output(in_motor_fwd_2, GPIO.LOW)
    GPIO.output(in_motor_fwd_3, GPIO.HIGH)
    GPIO.output(in_motor_fwd_4, GPIO.LOW)
    GPIO.output(in_motor_bkd_1, GPIO.LOW)
    GPIO.output(in_motor_bkd_2, GPIO.LOW)
    GPIO.output(in_motor_bkd_3, GPIO.LOW)
    GPIO.output(in_motor_bkd_4, GPIO.LOW)

def backward_move():
    GPIO.output(in_motor_fwd_1, GPIO.LOW)
    GPIO.output(in_motor_fwd_2, GPIO.HIGH)
    GPIO.output(in_motor_fwd_3, GPIO.LOW)
    GPIO.output(in_motor_fwd_4, GPIO.HIGH)
    GPIO.output(in_motor_bkd_1, GPIO.LOW)
    GPIO.output(in_motor_bkd_2, GPIO.LOW)
    GPIO.output(in_motor_bkd_3, GPIO.LOW)
    GPIO.output(in_motor_bkd_4, GPIO.LOW)

def side_fwd_move():
    GPIO.output(in_motor_fwd_1, GPIO.LOW)
    GPIO.output(in_motor_fwd_2, GPIO.LOW)
    GPIO.output(in_motor_fwd_3, GPIO.LOW)
    GPIO.output(in_motor_fwd_4, GPIO.LOW)
    GPIO.output(in_motor_bkd_1, GPIO.HIGH)
    GPIO.output(in_motor_bkd_2, GPIO.LOW)
    GPIO.output(in_motor_bkd_3, GPIO.HIGH)
    GPIO.output(in_motor_bkd_4, GPIO.LOW)

def side_bkd_move():
    GPIO.output(in_motor_fwd_1, GPIO.LOW)
    GPIO.output(in_motor_fwd_2, GPIO.LOW)
    GPIO.output(in_motor_fwd_3, GPIO.LOW)
    GPIO.output(in_motor_fwd_4, GPIO.LOW)
    GPIO.output(in_motor_bkd_1, GPIO.LOW)
    GPIO.output(in_motor_bkd_2, GPIO.HIGH)
    GPIO.output(in_motor_bkd_3, GPIO.LOW)
    GPIO.output(in_motor_bkd_4, GPIO.HIGH)

def speed_med():
    pwm_1.ChangeDutyCycle(75)
    pwm_2.ChangeDutyCycle(75)
    pwm_3.ChangeDutyCycle(75)
    pwm_4.ChangeDutyCycle(75)
def speed_full():
    pwm_1.ChangeDutyCycle(100)
    pwm_2.ChangeDutyCycle(100)
    pwm_3.ChangeDutyCycle(100)
    pwm_4.ChangeDutyCycle(100)

def start_setup():
    pwm_1.start(100)
    pwm_2.start(100)
    pwm_3.start(100)
    pwm_4.start(100)
    GPIO.output(ena_a_low, GPIO.HIGH)
    GPIO.output(ena_b_low, GPIO.HIGH)
    GPIO.output(ena_a_high, GPIO.HIGH)
    GPIO.output(ena_b_high, GPIO.HIGH) 


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

            sleep(0.2)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    stop_move()
    GPIO.cleanup()
    
main()
