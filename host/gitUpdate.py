# ===============================================================================================
# gitUpdate.py
# ===============================================================================================
# Description: updates the code all of the listed raspberry Pi's to the corrent github version
#
# Run Command: "python gitUpdate.py"
#
# Written By: Guadalupe Bernal
# Date Last Eddited: 07/07/2023
# ===============================================================================================


import subprocess
import json

def read_config_file(file_path):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data

# Assuming 'config.json' is in the same directory as the script.
# Modify the file path accordingly if it's located elsewhere.
config_data = read_config_file("config.json")

# array of Raspberry Pi IP addresses, add more IP addresses as needed
rpis = config_data["rpis"]

# directory of git repository on Raspberry Pis
repo_dir = "/home/pi/RPiCameraMotionDetection"

# SSH username
username = "pi"

# SSH and git pull on each Raspberry Pi
for rpi in rpis:
    print(f"Pulling latest code from repository on Raspberry Pi at {rpi}")

    # construct the SSH command
    # ssh_command = f'ssh {username}@{rpi} "cd {repo_dir} && git stash"'
    ssh_command = f'ssh {username}@{rpi}.local "cd {repo_dir} && git pull"'

    # run the SSH command using subprocess
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)

    # print the output of the git pull command
    if process.returncode == 0:
        print(process.stdout.strip())
    else:
        print(process.stderr.strip())
