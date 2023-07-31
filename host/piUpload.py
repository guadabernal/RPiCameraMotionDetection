# ===============================================================================================
# copyFiles.py
# ===============================================================================================
# Description: copies the saved videos onto a local directory and erases them
#
# Run Command: "python copyFiles.py"
#
# Written By: Guadalupe Bernal
# Date Last Eddited: 07/07/2023
# ===============================================================================================


import subprocess
import os
import time
import json
import re

def read_config_file(file_path):
    with open(file_path, 'r') as config_file:
        config_data = json.load(config_file)
    return config_data

# Assuming 'config.json' is in the same directory as the script.
# Modify the file path accordingly if it's located elsewhere.
config_data = read_config_file("config.json")

# array of Raspberry Pi IP addresses, add more IP addresses as needed
rpis = config_data["rpis"]

# source directory on the Raspberry Pi
source_dir = "~/videos"

# destination directory on the local machine
destination_dir = "pi@10.0.0.1:~/videos"

box_dir = "Napp Lab/Bee Entrance Data/BeeMonitoring/"

# rclone copy . --include "*"  box:"Napp Lab/Bee Entrance Data/BeeMonitoring/2023_TRIAL_01" 

print("------------------------------------------------------------------------------------------")
print("Stop recording...")
print("------------------------------------------------------------------------------------------")

for rpi in rpis:

    ssh_addr = f'pi@{rpi}.local'


    print(f"{ssh_addr}")
     # construct the SSH command to get the file count
    ssh_command = f'ssh {ssh_addr} "~/stop_recording.sh"'
    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        if process.stderr:
            print(process.stderr)
        print(process.stdout.strip())
    
    except:
        print(f"   Error accessing {rpi}")
        continue


print("------------------------------------------------------------------------------------------")
print("Downloading...")
print("------------------------------------------------------------------------------------------")

# SCP the content of video folder from each Raspberry Pi
for rpi in rpis:
    ssh_addr = f'pi@{rpi}.local'

    print(f"{ssh_addr}")
    print(f"  Calculating the number of files and total size to be copied...")

    # construct the SSH command to get the file count
    ssh_command = f'ssh {ssh_addr} "find {source_dir} -type f | wc -l"'

    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        file_count = int(process.stdout.strip())
        print(f"  Successfully accessed {ssh_addr}")
    except:
        print(f"  Error accessing {ssh_addr}")
        continue

    if file_count == 0:
        print("  Error No files in the folder")
        continue

    # construct the SSH command to get the total size
    ssh_command = f'ssh {ssh_addr} "du -bs {source_dir} | awk \'{{print $1}}\'"'

    # run the SSH command to get the total size
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    total_size_output = re.sub(r'\D', '', process.stdout.strip())
    total_size = int(total_size_output) if total_size_output else 0
    
    # estimate the copy time
    copy_time = total_size / (1 * 1024 * 1024)  # Assuming average transfer rate of 1 MB/s

    print(f"  Number of files to be copied: {file_count}")
    print(f"  Total size to be copied: {total_size} bytes")
    print(f"  Estimated copy time: {copy_time:.2f} seconds assuming 10Mb/s")

    print(f"  Copying files from {ssh_addr}:{source_dir} to {destination_dir} folder on the local machine")

    # create the destination directory if it doesn't exist
    dd = f"{destination_dir}"
    os.makedirs(dd, exist_ok=True)

    start_time = time.time()

    # construct the SCP command
    scp_command = f'scp -r {ssh_addr}:{source_dir}/* {destination_dir}'

    # run the SCP command using subprocess
    process = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

    end_time = time.time()

    # print output of the SCP command
    if process.returncode == 0:
        print(f"  Files from {ssh_addr} copied successfully to {rpi} folder on the local machine")
        print(f"  Actual copy time: {end_time - start_time:.2f} seconds")
    else:
        print(f"  Failed to copy files from {ssh_addr}:{source_dir} to {rpi} folder on the local machine")
        print("  " + process.stderr.strip())

    print("------------------------------------------------------------------------------------------")
