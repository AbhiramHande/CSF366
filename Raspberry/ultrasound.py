import keyboard
import RPi.GPIO as GPIO
import time

# Define GPIO Pins
TRIG = 27  
ECHO = 22  

# Setup GPIO Mode
def setup_ultrasound():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for the echo signal to go LOW
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # in cm
    return round(distance, 2)

# Test the sensors if directly run
if __name__ == "__main__":
    setup_ultrasound()
    time = 0
    try:
        while True:
            if keyboard.is_pressed('d'):
                elapsed_time = 0
                dist = measure_distance()
                print(f"Distance: {dist} cm")
                time.sleep(0.2)
            elif keyboard.is_pressed('q'):
                print("Exiting...")
                break
            else:
                elapsed_time += 1
                print(f"Waiting for input... ({elapsed_time}s elapsed)", end='\r')
                time.sleep(1)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        print("Measurement stopped by user.")
        GPIO.cleanup()
