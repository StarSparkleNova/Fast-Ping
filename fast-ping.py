# Import necessary modules
import ipaddress
from ping3 import ping
import concurrent.futures
import threading
import logging
import multiprocessing

# Configure the logging module to display log messages
logging.basicConfig(level=logging.INFO)

# Define a function to ping an IP address and handle retries for failed pings
def ping_ip(ip, results, lock, timeout=1, max_retries=3):
    for _ in range(max_retries):
        try:
            # Attempt to ping the IP address
            response_time = ping(str(ip), timeout=timeout)
            
            # If a response is received, log it and add the IP to the results list
            if response_time is not None:
                logging.info(f'{ip} is reachable (Response time: {response_time} ms)')
                with lock:
                    results.append(ip)
                break  # Break the loop if successful

        # Catch and log any exceptions that occur during the ping
        except Exception as e:
            logging.error(f'Error pinging {ip}: {str(e)}')

# Define the main function to ping a custom IP range
def ping_custom_range(start_ip, end_ip, max_threads=None):
    try:
        # Parse and validate the start and end IP addresses
        start_ip = ipaddress.IPv4Address(start_ip)
        end_ip = ipaddress.IPv4Address(end_ip)
    except ipaddress.AddressValueError:
        print("Invalid IP address format.")
        return

    # Ensure the ending IP address is greater than or equal to the starting IP address
    if end_ip < start_ip:
        print("Ending IP address should be greater than or equal to the starting IP address.")
        return

    # Create a list of IP addresses within the specified range
    ip_range = list(ipaddress.IPv4Address(ip) for ip in range(int(start_ip), int(end_ip) + 1))

    # Initialize a list to store reachable IP addresses and a lock for thread safety
    reachable_ips = []
    lock = threading.Lock()

    # Determine the number of CPU cores
    num_cores = multiprocessing.cpu_count()

    # Set the maximum thread pool size based on available CPU cores
    if max_threads is None:
        max_threads = num_cores * 64  # Use 64 threads per core

    # Print the number of threads to be used for pinging
    print(f"Using {max_threads} threads for pinging.")

    # Create a thread pool and submit ping tasks for each IP address in the range
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        for ip in ip_range:
            executor.submit(ping_ip, ip, reachable_ips, lock)

    # Display the list of reachable IP addresses
    print("\nList of reachable IP addresses:")
    for ip in reachable_ips:
        print(ip)

# Entry point of the program
if __name__ == "__main__":
    start_ip = input("Enter the starting IP address: ")
    end_ip = input("Enter the ending IP address: ")
    timeout = int(input("Enter the timeout (default is 1 second): ") or 1)  # Allow custom timeout input

    # Call the main function to ping the specified IP range
    ping_custom_range(start_ip, end_ip)

