# ===============================================================================================
# deleteFiles.py
# ===============================================================================================
# Description: copys the saved videos onto a local directory and erases them
#
# Run Command: "python deleteFiles.py"
#
# Written By: Guadalupe Bernal
# Date Last Eddited: 07/07/2023
# ===============================================================================================


import subprocess
import json
import os
import time

def read_config_file(file_path):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data

# Assuming 'config.json' is in the same directory as the script.
# Modify the file path accordingly if it's located elsewhere.
config_data = read_config_file("config.json")

# array of Raspberry Pi IP addresses, add more IP addresses as needed
rpis = config_data["rpis"]

# SSH username
username = "pi"

# source directory on the Raspberry Pi
source_dir = "/home/pi/videos"

print("------------------------------------------------------------------------------------------")
print("Removing video files...")
print("------------------------------------------------------------------------------------------")

for rpi in rpis:
    print(f"{rpi}")
     # construct the SSH command to get the file count
    # ssh_command = f'ssh {rpi} "rm -rf {source_dir}"'
    ssh_command = f'ssh {username}@{rpi}.local "cd {source_dir} && rm -rf *"'

    # run the SSH command using subprocess
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)

    # print the output of the git pull command
    if process.returncode == 0:
        print(process.stdout.strip())
    else:
        print(process.stderr.strip())