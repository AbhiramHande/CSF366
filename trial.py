#A simple program to test whether the cloning and execution on the Raspberry Pi works fine
from gpiozero import LED
from time import sleep

def main():
    led = LED(17)

    for _ in range(16):
        led.on()
        print(f"GPIO17 is {'HIGH' if led.is_active else 'LOW'}")
        sleep(1)
        led.off()
        print(f"GPIO17 is {'HIGH' if led.is_active else 'LOW'}")
        sleep(1)

main()
