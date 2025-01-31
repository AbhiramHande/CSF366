import RPi.GPIO as GPIO
from time import sleep

#Test the motors
ena = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(ena, GPIO.OUT)
pwm = GPIO.PWM(ena, 1000)  # 1 kHz PWM frequency
pwm.start(50) 

print("PWM is running at 50% duty cycle")
sleep(5)
pwm.stop()
GPIO.cleanup()
print("Test complete.")
