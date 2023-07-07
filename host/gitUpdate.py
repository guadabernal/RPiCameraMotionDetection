import subprocess

# Array of Raspberry Pi IP addresses
rpis = ["bee01", "bee02", "bee01"]

# Directory of the git repository on the Raspberry Pis
repo_dir = "/home/pi/RPiCameraMotionDetection"

# SSH username
username = "pi"

# SSH and git pull on each Raspberry Pi
for rpi in rpis:
    print(f"Pulling latest code from repository on Raspberry Pi at {rpi}")

    # Construct the SSH command
    ssh_command = f'ssh {username}@{rpi} "cd {repo_dir} && git pull"'

    # Run the SSH command using subprocess
    process = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)

    # Print the output of the git pull command
    if process.returncode == 0:
        print(process.stdout.strip())
    else:
        print(process.stderr.strip())
