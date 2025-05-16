import keyboard
import Jetson.GPIO as GPIO
from time import sleep, time

# Define GPIO Pins
front_trig = 21           # Physical pin 40
front_echo = 20           # Physical pin 38

side_trig = 6             # Physical pin 31
side_echo = 5             # Physical pin 29

# Setup GPIO Mode
def setup_ultrasound():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(front_trig, GPIO.OUT)
    GPIO.setup(front_echo, GPIO.IN)
    GPIO.setup(side_trig, GPIO.OUT)
    GPIO.setup(side_echo, GPIO.IN)

# Function to measure front sensor distance
def measure_front_distance():
    GPIO.output(front_trig, False)
    sleep(0.1)
    GPIO.output(front_trig, True)
    sleep(0.00001)
    GPIO.output(front_trig, False)

    while GPIO.input(front_echo) == 0:
        pulse_start = time()

    # Wait for the echo signal to go LOW
    while GPIO.input(front_echo) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # in cm
    return round(distance, 2)

# Function to measure side sensor distance
def measure_side_distance():
    GPIO.output(side_trig, False)
    sleep(0.1)
    GPIO.output(side_trig, True)
    sleep(0.00001)
    GPIO.output(side_trig, False)

    while GPIO.input(side_echo) == 0:
        pulse_start = time()

    # Wait for the echo signal to go LOW
    while GPIO.input(side_echo) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # in cm
    return round(distance, 2)

# Test the sensors if directly run
if __name__ == "__main__":
    setup_ultrasound()
    elapsed_time = 0
    try:
        while True:
            print(f"Waiting for input... ({elapsed_time}s elapsed)", end='\r')
            if keyboard.is_pressed('d'):
                elapsed_time = 0
                # Run distance measurements in parallel using threads
                dist = measure_front_distance()
                print(f"\nFront Distance: {dist} cm")
                dist = measure_side_distance()
                print(f"\nSide Distance: {dist} cm")
                sleep(0.2)
            elif keyboard.is_pressed('q'):
                print("\nExiting...")
                break
            else:
                elapsed_time += 1
                print(f"Waiting for input... ({elapsed_time}s elapsed)", end='\r')
                sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        print("Measurement stopped by user.")
        GPIO.cleanup()