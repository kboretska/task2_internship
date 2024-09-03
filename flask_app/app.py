from flask import Flask, render_template, jsonify
import subprocess
import re
from collections import defaultdict

app = Flask(__name__)

# IP addresses of the machines
hosts = ["sftp_1"]

# Command to list files in the directory
list_command = "ls -1 /home/sftp/uploads"

# Regular expression to extract server number from the file name
file_pattern = re.compile(r"^sftp-(\d+)_file_\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}\.txt$")

def execute_command(host, command):
    """
       Execute a command via vagrant ssh on a given host.
       Returns: str: The standard output of the command as a string.
       Raises: RuntimeError: If the command fails, an error message is raised.
    """
    result = subprocess.run(
        ["vagrant", "ssh", host, "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to connect to {host}: {result.stderr.strip()}")

    return result.stdout.splitlines()

def parse_files(file_list):
    """
       Parse the list of files and group them by server number. 
       Returns:dict: A dictionary where keys are server numbers and values are lists of file dictionaries.
    """
    server_files = defaultdict(list)

    for file in file_list:
        match = file_pattern.match(file)
        if match:
            server_number = match.group(1)
            server_files[server_number].append({"name": file})

    return server_files

def get_server_files(host):
    """
       Get the files from the /home/sftp/uploads directory on a given host.
       Returns: dict: A dictionary with files grouped by server number, or an error dictionary if an error occurs.
    """
    try:
        file_list = execute_command(host, list_command)
        return parse_files(file_list)
    except RuntimeError as e:
        return {"error": str(e)}

def aggregate_total_counts(server_files_list):
    """
       Aggregate total file counts across all servers.
       Returns: dict: A dictionary where keys are server numbers and values are total file counts.
    """
    total_counts = defaultdict(int)
    for server_files in server_files_list:
        for server_number, files in server_files.items():
            total_counts[server_number] += len(files)
    return total_counts

@app.route('/stats', methods=['GET'])
def get_stats():
    """
    Endpoint to retrieve and render statistics of files across servers.

    Returns: Response: Rendered HTML template with file statistics, or an error response if an error occurs.
    """
    server_files_list = []
    results = {}

    for host in hosts:
        server_files = get_server_files(host)
        if "error" in server_files:
            return jsonify(server_files), 500

        server_files_list.append(server_files)

        # Remove the current host from server_files to avoid reporting on itself
        server_number = host.split('_')[1]
        server_files.pop(server_number, None)
        
        results[host] = {
            "files": server_files
        }

    # Add total counts to the results
    total_counts = aggregate_total_counts(server_files_list)
    results['total'] = total_counts

    return render_template('stats.html', stats=results)

if __name__ == '__main__':
    app.run(debug=True)
