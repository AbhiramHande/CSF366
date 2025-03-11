#!/bin/bash

# Setup system variables
SSID="wifi_name"
PASSWORD="wifi_password"
REPO_PATH="/home/inspire/Documents/Project/source_code"
IP_FILE="ip_address.txt"

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
        echo "SSID not found" >> "$REPO_PATH"/tmp/dump.txt
        exit 1
    fi
    
    if ! nmcli dev wifi connect "$SSID" password "$PASSWORD"; then
        echo "Connection failed" >> "$REPO_PATH"/tmp/dump.txt
        exit 1
    fi

    echo "Successfully connected to WiFi" >> "$REPO_PATH"/tmp/dump.txt
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
    echo "$IP" > "$REPO_PATH"/tmp/"$OUTPUT_FILE"
}

# Function to git push
git_push() {
    cd $REPO_PATH || exit 1
    git config --global user.name "Jetson Auto Committer"
    git config --global user.email "auto@example.com"
    git add $OUTPUT_FILE
    git commit -m "Automatic IP update: $(date)"
    git push origin main
}

# Main execution
git_pull
> "$REPO_PATH"/tmp/dump.txt
touch /boot/ssh
connect_wifi
get_and_save_ip
git_update
