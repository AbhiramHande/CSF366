#A simple program to test whether the cloning and execution on the Raspberry Pi works fine

import datetime

def main():
    now = datetime.datetime.now()
    print("Hello, world! This program was executed successfully.")
    print(f"Current date and time: {now}")

main()
