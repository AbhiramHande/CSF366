#!/bin/bash

# Setup system variables
SSID="wifi_name"
PASSWORD="wifi_password"
REPO_PATH="/home/inspire/Documents/Project/source_code"
IP_FILE="ip_address.txt"
DUMP_FILE="/home/inspire/Desktop/dump.txt"

git_pull(){
    cd "$REPO_PATH" || exit 1
    git fetch --all
    git reset --hard origin/main
    git clean -fd
}

# Function to connect to WiFi
connect_wifi() {
    nmcli device wifi rescan
    if ! nmcli device wifi list | grep -q $SSID; then
        echo "SSID not found" >> "$DUMP_FILE"
        exit 1
    fi
    
    if ! nmcli dev wifi connect "$SSID" password "$PASSWORD"; then
        echo "Connection failed" >> "$DUMP_FILE"
        exit 1
    fi

    echo "Successfully connected to WiFi" >> "$DUMP_FILE"
}

# Function to get and save IP
get_and_save_ip() {
    # Wait for connection
    while true; do
        IP=$(hostname -I | awk '{print $1}')
        [ -n "$IP" ] && break
        sleep 2
    done

    # Write IP to file
    mkdir -p  "$REPO_PATH"/tmp
    echo "$IP" > "$REPO_PATH"/tmp/"$IP_FILE"
}

# Function to git push
git_push() {
    cd $REPO_PATH || exit 1
    git config --global user.name "Jetson Auto Committer"
    git config --global user.email "auto@example.com"
    git add .
    git commit -m "Automatic IP update: $(date)"
    git push origin main
}

# Main execution
> "$DUMP_FILE"
touch /boot/ssh
connect_wifi
git_pull
get_and_save_ip
git_push
