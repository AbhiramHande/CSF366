#!/bin/bash

# Setup system variables
SSID="wifi_name"
PASSWORD="wifi_password"
REPO_PATH="/home/inspire/Documents/Project/CSF366"
IP_FILE="ip_address.txt"

# Enable SSH
touch /boot/ssh

# Configure WiFi
cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
country=IN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="$SSID"
    psk="$PASSWORD"
}
EOF

chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
wpa_cli -i wlan0 reconfigure
sleep 20

# Get IP Address
IP_ADDR=$(hostname -I | awk '{print $1}')
echo "$IP_ADDR" > /tmp/device_ip.txt

if [ ! -d "$REPO_PATH" ]; then
    echo "Error: Directory does not exist."
    exit 1
else
    cd "$REPO_PATH"
    mkdir -p tmp
    echo "$IP_ADDR" > tmp/$IP_FILE
    git add tmp/$IP_FILE
    git commit -m "Update IP Address"
    git push origin main

    echo "Setup done!"
fi