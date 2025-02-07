#!/bin/bash

if [ $(uname -r | grep -c 'rpi') -ge 1 ]; then
    sudo python3 rpi_trial.py
elif [ $(uname -r | grep -c 'tegra') -ge 1 ]; then 
    sudo python3 jetson_trial.py
fi
