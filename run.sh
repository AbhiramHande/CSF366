#!/bin/bash

if [ "$(uname -r | grep -c 'rpi')" -ge 1 ]; then
    sudo python3 Raspberry/ultrasound.py
elif [ "$(uname -r | grep -c 'tegra')" -ge 1 ]; then 
    sudo python3 Jetson/motor.py
    #sudo python3 Jetson/ultrasound.py
fi
