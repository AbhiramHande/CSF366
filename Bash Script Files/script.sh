#!/bin/bash

REPO_URL="https://github.com/AbhiramHande/CSF366"        # URL to GitHub repository
REPO_DIR="/home/pi/Project/source_code"                  # Path to your local repository
BRANCH="main"                                            # Branch you want to update

clone_repository(){
    git clone "$REPO_URL" "$REPO_DIR"
}

check_and_navigate_to_directory() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Directory does not exist. Cloning repository."
        clone_repository
    fi
    cd "$REPO_DIR" || { 
        echo "Error: Failed to navigate to $REPO_DIR";
        exit 1;
    }
}

update_repository() {
    git fetch --all
    git reset --hard origin/"$BRANCH"
    git clean -fd
}

run_program() {
    NUM_SH_FILES=$(ls -1 *.sh | wc -l)
    if [ "$NUM_SH_FILES" -eq 0 ]; then
        echo "No bash file found."
        exit 1
    elif [ "$NUM_SH_FILES" -eq 1 ]; then
    	SCRIPT=$(ls -1 *.sh)
    	echo "Running $SCRIPT..."
        chmod +x "$SCRIPT"
        ./"$SCRIPT"
    else
        echo "Multiple script files found: Kindly select the relevant one."
        ls -1 *.sh
        read -p "Enter the script number you want to run: " INPUT
        
	if [ "$INPUT" -lt 1 ] || [ "$INPUT" -gt "$NUM_SH_FILES" ]; then
	    echo "Error: Invalid input."
	    exit 1
	else
	    SCRIPT=$(ls -1 *.sh | head -n "$INPUT" | tail -1)
	    echo "Running $SCRIPT..."
	    chmod +x "$SCRIPT"
	    ./"$SCRIPT"
	fi
    fi
}

main() {
    check_and_navigate_to_directory
    update_repository
    run_program
}

main