# ===============================================================================================
# stopRecording.py
# ===============================================================================================
# Description: stop recordings on all pis
#
# Run Command: "python stopRecording.py"
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

print("------------------------------------------------------------------------------------------")
print("Stop recording...")
print("------------------------------------------------------------------------------------------")

for rpi in rpis:
    print(f"{rpi}")
     # construct the SSH command to get the file count
    ssh_command = f'ssh pi@{rpi}.local "~/stop_recording.sh"'
    try:
        # run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        if process.stderr:
            print(process.stderr)
    except subprocess.CalledProcessError as e:
        print(f"   Error accessing {rpi}")
        continue