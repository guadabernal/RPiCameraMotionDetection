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

# source directory on the Raspberry Pi
source_dir = "~/videos"

# destination directory on the local machine
destination_dir = "pi@10.0.0.1:~/videos"
ssh_addr = "pi@10.0.0.1"

box_dir = "Napp Lab/Bee Entrance Data/BeeMonitoring/2023_TRIAL_01"

print("------------------------------------------------------------------------------------------")
print("Uploading...")
print("------------------------------------------------------------------------------------------")

# SCP the content of video folder from each Raspberry Pi
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
  exit()

if file_count == 0:
  print("  Error No files in the folder")
  exit()

# construct the SSH command to get the total size
ssh_command = f'ssh {ssh_addr} "du -bs {source_dir} | awk \'{{print $1}}\'"'

# run the SSH command to get the total size
process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
total_size_output = re.sub(r'\D', '', process.stdout.strip())
total_size = int(total_size_output) if total_size_output else 0

# estimate the copy time
copy_time = total_size / (1 * 1024 * 1024)  # Assuming average transfer rate of 1 MB/s

print(f"  Number of files to be uploaded: {file_count}")
print(f"  Total size to be uploaded: {total_size} bytes")
print(f"  Estimated upload time: {copy_time:.2f} seconds assuming 10Mb/s")

print(f"  Uploading files from {ssh_addr}:{source_dir} to {box_dir} folder in box")

start_time = time.time()

# construct the SCP command


box_dir = "Napp Lab/Bee Entrance Data/BeeMonitoring/2023_TRIAL_01"
print(box_dir)
cpy_command = f'cd {source_dir} && rclone copy . --include "*"  box:"{box_dir}"'
print(cpy_command)
scp_command = f"ssh {ssh_addr} '{cpy_command}'"
print(scp_command)
# exit()
# run the SCP command using subprocess
process = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

end_time = time.time()

# print output of the SCP command
if process.returncode == 0:
    print(f"  Files from {ssh_addr}:{source_dir} to box folder")
    print(f"  Actual copy time: {end_time - start_time:.2f} seconds")
else:
    print(f"  Failed to copy files from {ssh_addr}:{source_dir} to box folder")
    print("  " + process.stderr.strip())

print("------------------------------------------------------------------------------------------")

ssh_command = f'ssh {ssh_addr} "cd {source_dir} && rm -rf *"'

# run the SSH command using subprocess
process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)

# print the output of the git pull command
if process.returncode == 0:
    print(process.stdout.strip())
else:
    print(process.stderr.strip())