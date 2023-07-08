# ===============================================================================================
# copyFiles.py
# ===============================================================================================
# Description: copys the saved videos onto a local directory and erases them
#
# Run Command: "python copyFiles.py"
# 
# Written By: Guadalupe Bernal 
# Date Last Eddited: 07/07/2023
# ===============================================================================================


import subprocess
import os
import time

# array of Raspberry Pi IP addresses, add more IP addresses as needed
rpis = ["bee01", "bee02"]

# source directory on the Raspberry Pi
source_dir = "~/videos"

# destination directory on the local machine
destination_dir = "./allvideos"                 # REPLACE


print("------------------------------------------------------------------------------------------")
print("Stop recording...")
print("------------------------------------------------------------------------------------------")

for rpi in rpis:
    print(f"{rpi}")
     # construct the SSH command to get the file count
    ssh_command = f'ssh {rpi} "~/stop_recording.sh"'
    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    except:
        print(f"   Error accessing {rpi}")
        continue
print("------------------------------------------------------------------------------------------")
print("Downloading...")
print("------------------------------------------------------------------------------------------")

# SCP the content of video folder from each Raspberry Pi
for rpi in rpis:
    
    print(f"{rpi}")
    print(f"  Calculating the number of files and total size to be copied...")

    # construct the SSH command to get the file count
    ssh_command = f'ssh {rpi} "find {source_dir} -type f | wc -l"'

    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        file_count = int(process.stdout.strip())
    except:
        print(f"  Error accessing {rpi}")
        continue
    
    if file_count == 0:
        print("  Error No files in the folder")
        continue

    # construct the SSH command to get the total size
    ssh_command = f'ssh {rpi} "du -bs {source_dir} | awk \'{{print $1}}\'"'

    # run the SSH command to get the total size
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    total_size_output = process.stdout.strip()
    total_size = int(total_size_output) if total_size_output else 0

    # estimate the copy time
    copy_time = total_size / (1 * 1024 * 1024)  # Assuming average transfer rate of 1 MB/s

    print(f"  Number of files to be copied: {file_count}")
    print(f"  Total size to be copied: {total_size} bytes")
    print(f"  Estimated copy time: {copy_time:.2f} seconds assuming 10Mb/s")

    print(f"  Copying files from {rpi}:{source_dir} to {destination_dir}/{rpi} folder on the local machine")

    # create the destination directory if it doesn't exist
    dd = f"{destination_dir}/{rpi}"
    os.makedirs(dd, exist_ok=True)

    start_time = time.time()

    # construct the SCP command
    scp_command = f'scp -r {rpi}:{source_dir}/* {destination_dir}/{rpi}'

    # run the SCP command using subprocess
    process = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

    end_time = time.time()

    # print output of the SCP command
    if process.returncode == 0:
        print(f"  Files from {rpi} copied successfully to {rpi} folder on the local machine")
        print(f"  Actual copy time: {end_time - start_time:.2f} seconds")
    else:
        print(f"  Failed to copy files from {rpi}:{source_dir} to {rpi} folder on the local machine")
        print("  " + process.stderr.strip())

    print("------------------------------------------------------------------------------------------")
