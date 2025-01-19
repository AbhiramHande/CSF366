# Laboratory Project - CS F366

This repository is for a **Robotics project** undertaken under Prof. Sudeept Mohan, Dept. of Computer Science and Information Systems, BITS Pilani, as part of the course **CS F366 - Laboratory Project**.

---

## **Bash Code: `script.sh`**

This is the `script.sh` bash script that you can use to update the local directory with the latest code from your GitHub repository and run the program. The script is stored in the repository to be restored in case it gets accidentally deleted from your Raspberry Pi.

```bash
#!/bin/bash

REPO_URL="https://github.com/AbhiramHande/CSF366"        # URL to GitHub repository
REPO_DIR="/home/pi/Project/source_code"                  # Path to your local repository
BRANCH="main"                                            # Branch you want to update

clone_repository(){
    echo "Cloning GitHub repository..."
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
    echo "Pulling the latest changes from the repository..."
    git fetch --all
    git reset --hard origin/"$BRANCH"
    git clean -fd
    echo "Repository updated successfully."
}

run_program() {
    echo "Finding bash file to execute the program..."
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
```

---

## **Usage**
1. **Create a `script.sh` file:**
   Open the script in your text editor to configure it:
   ```bash
   nano script.sh
   ```
   Update the following variables as needed:
   - `REPO_URL`: URL of your GitHub repository.
   - `REPO_DIR`: Path to the local directory where the repository is stored.
   - `BRANCH`: The branch to pull updates from.
   - `EXECUTABLE`: The name of the program you want to run.

2. **Make the script executable:**
   ```bash
   chmod +x script.sh
   ```

3. **Run the script:**
   ```bash
   ./script.sh
   ```

---

## **Prerequisites**
- Raspberry Pi with Raspberry Pi OS (or any Linux distribution) installed.
- Python 3 installed (for running Python programs).
- Git installed on the Raspberry Pi:
  ```bash
  sudo apt update && sudo apt install git
  ```

---

## **Currently Working On:**
- Controlling the GPIO pins of the Raspberry Pi.
- Using the LM298 Motor driver to control the movement of the robot.
