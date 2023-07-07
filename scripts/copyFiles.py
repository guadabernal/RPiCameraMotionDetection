import subprocess
import os
import time

# Array of Raspberry Pi IP addresses
rpis = ["bee01", "bee02"]  # Add more IP addresses as needed

# Source directory on the Raspberry Pi
source_dir = "~/videos"  # Replace with the actual path to the videos directory

# Destination directory on the local machine
destination_dir = "./allvideos"  # Replace with the desired local destination directory

print("------------------------------------------------------------------------------------------")
print("Downloading...")
print("------------------------------------------------------------------------------------------")

# SCP the content of the video folder from each Raspberry Pi
for rpi in rpis:
    print(f"{rpi}")
    print(f"  Calculating the number of files and total size to be copied...")
    
    # Construct the SSH command to get the file count
    ssh_command = f'ssh {rpi} "find {source_dir} -type f | wc -l"'

    try:
        # Run the SSH command to get the file count
        process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
        file_count = int(process.stdout.strip())
    except:
        print(f"   Error accessing {rpi}")
        continue

    # Construct the SSH command to get the total size
    ssh_command = f'ssh {rpi} "du -bs {source_dir} | awk \'{{print $1}}\'"'
    # Run the SSH command to get the total size
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    total_size_output = process.stdout.strip()
    total_size = int(total_size_output) if total_size_output else 0

    # Estimate the copy time
    copy_time = total_size / (1 * 1024 * 1024)  # Assuming average transfer rate of 1 MB/s

    print(f"  Number of files to be copied: {file_count}")
    print(f"  Total size to be copied: {total_size} bytes")
    print(f"  Estimated copy time: {copy_time:.2f} seconds assuming 10Mb/s")

    print(f"  Copying files from {rpi}:{source_dir} to {destination_dir}/{rpi} folder on the local machine")

    # Create the destination directory if it doesn't exist
    dd = f"{destination_dir}/{rpi}"
    os.makedirs(dd, exist_ok=True)

    start_time = time.time()

    # Construct the SCP command
    scp_command = f'scp -r {rpi}:{source_dir}/* {destination_dir}/{rpi}'

    # Run the SCP command using subprocess
    process = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

    end_time = time.time()

    # Print the output of the SCP command
    if process.returncode == 0:
        print(f"  Files from {rpi} copied successfully to {rpi} folder on the local machine")
        print(f"  Actual copy time: {end_time - start_time:.2f} seconds")
    else:
        print(f"  Failed to copy files from {rpi}:{source_dir} to {rpi} folder on the local machine")
        print("  " + process.stderr.strip())

    print("------------------------------------------------------------------------------------------")
