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
import os
import time

# array of Raspberry Pi IP addresses, add more IP addresses as needed
rpis = ["bee01", "bee02"]

# source directory on the Raspberry Pi
source_dir = "~/videos"

print("------------------------------------------------------------------------------------------")
print("Removing video files...")
print("------------------------------------------------------------------------------------------")

for rpi in rpis:
    print(f"{rpi}")
     # construct the SSH command to get the file count
    ssh_command = f'ssh {rpi} "rm -rf {source_dir}"'

    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    except:
        print(f"   Error accessing {rpi}")
        continue