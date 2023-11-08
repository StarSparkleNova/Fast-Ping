This Python script is a simple yet powerful tool for pinging a range of IP addresses concurrently.
It allows you to specify a starting and ending IP address and utilizes multithreading to ping multiple IPs simultaneously. 
The tool dynamically adjusts the number of threads based on the available CPU cores to optimize performance.

Key Features:

    Pings a range of IP addresses concurrently.
    Adjustable timeout for network responsiveness.
    Dynamic thread pool size based on the number of CPU cores.
    Handles errors gracefully and supports a retry mechanism.
    Logs reachable IPs with response times.

Usage:

    Run the script.
    Enter the starting and ending IP addresses.
    Optionally, set the timeout for pinging (default is 1 second).
    The script will ping the specified IP range and display reachable IP addresses.
