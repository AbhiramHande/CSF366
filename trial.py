#A simple program to test whether the cloning and execution on the Raspberry Pi works fine
from gpiozero import LED
from time import sleep

def main():
    led = LED(17)
    
    for _ in range(16):
        led.on()
        sleep(1)
        led.off()
        sleep(1)

main()
