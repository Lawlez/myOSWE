import os
import subprocess
import threading
import queue

# function to scan for open ports using nmap
def scan(ip, output_queue):
    open_ports = []
    # Execute Nmap command as subprocess
    cmd = f"nmap -sS --open -T4 {ip}"
    output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    print(output)
    # Parse output to obtain open ports
    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            port = int(line.split("/")[0])
            open_ports.append(port)
            # Output each open port and banner as it is discovered
            banner = get_banner(ip, port)
            print(f"Port: {port}\t Banner: {banner}")
            # Add open port and banner to output queue
            output_queue.put(f"Port: {port}\t Banner: {banner}")
    return open_ports

# function to get banner of open port using netcat
def get_banner(ip, port):
    cmd = (f'echo "" | nc -w 2 {ip} {port}')
    banner = subprocess.Popen(cmd)
    print(banner)
    banner.kill()
    return banner

# function to write output to file asynchronously
def write_to_file(output_queue):
    with open("report.txt", "w") as file:
        while True:
            # Get output from queue and write it to file
            output = output_queue.get()
            if output is None:
                break
            file.write(output + "\n")

if __name__ == '__main__':
    ip = '10.10.11.8' #input('Enter IP address to scan: ')
    output_queue = queue.Queue()
    # Start thread to write output to file asynchronously
    write_thread = threading.Thread(target=write_to_file, args=(output_queue,))
    write_thread.start()
    open_ports = scan(ip, output_queue)
    # Signal end of output to file thread
    output_queue.put(None)
    # Wait for output to file thread to finish
    write_thread.join()
    print("Report written to file: report.txt")
