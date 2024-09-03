import subprocess
import re
from collections import defaultdict

# IP addresses of the machines
hosts = ["sftp_1", "sftp_2", "sftp_3"]

# Command to list files in the directory
command = "ls -1 /home/sftp/uploads"

# Regular expression to extract server number from the file name
file_pattern = re.compile(r"^sftp-(\d+)_file_\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.txt$")

def count_files_per_server(host):
    """Count the number of files made by each server in the /home/sftp/uploads directory on a given host."""
    try:
        # Execute the command via vagrant ssh
        result = subprocess.run(
            ["vagrant", "ssh", host, "-c", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"Failed to connect to {host}: {result.stderr.strip()}")
            return None

        file_list = result.stdout.splitlines()
        server_entries = defaultdict(int)
        
        for file in file_list:
            match = file_pattern.match(file)
            if match:
                server_number = match.group(1)
                server_entries[server_number] += 1

        return server_entries

    except Exception as e:
        print(f"Failed to connect to {host}: {str(e)}")
        return None

if __name__ == "__main__":
    total_entries = defaultdict(int)

    for host in hosts:
        entries = count_files_per_server(host)
        if entries is not None:
            # Remove the current host from entries to avoid reporting on itself
            entries.pop(host.split('_')[1], None)
            
            # Print entries for the current host
            entries_str = ", ".join(f"server_{server} made {count} entries" for server, count in entries.items())
            print(f"{host} server: {entries_str}.")
            
            # Update total_entries
            for server, count in entries.items():
                total_entries[server] += count

    # Print total statistics
    print("\nTotal statistics:")
    for server, count in total_entries.items():
        print(f"server_{server} made {count} entries in total.")
