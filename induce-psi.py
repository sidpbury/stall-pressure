import os
import random
import string
import subprocess
import time
import multiprocessing
import psutil
import matplotlib.pyplot as plt

def read_psi_info():
    """Reads the PSI (Pressure Stall Information) data."""
    psi_paths = {
        'cpu': '/proc/pressure/cpu',
        'memory': '/proc/pressure/memory',
        'io': '/proc/pressure/io'
    }

    psi_data = {}

    for resource, path in psi_paths.items():
        print(f"Checking if {path} exists...")
        if os.path.exists(path):
            print(f"{path} exists, reading data...")
            try:
                with open(path, 'r') as f:
                    lines = f.readlines()
                    print(f"Raw data from {resource}: {lines}")  # Print raw data from the file

                    if not lines:
                        print(f"Warning: {resource} pressure data is empty.")
                        psi_data[resource] = None
                    else:
                        data = {}
                        for line in lines:
                            line = line.strip()
                            # If there are multiple key-value pairs on the same line, split by space
                            for part in line.split(' '):
                                if '=' in part:
                                    key, value = part.split('=')
                                    try:
                                        value = float(value)
                                        data[key] = value
                                    except ValueError:
                                        print(f"Warning: Unable to convert value '{value}' to float.")
                        # If no data is found, mark it as None
                        if not data:
                            print(f"Warning: No valid data found for {resource}.")
                            psi_data[resource] = None
                        else:
                            psi_data[resource] = data
            except Exception as e:
                print(f"Error reading {resource} pressure data: {str(e)}")
                psi_data[resource] = None
        else:
            print(f"Warning: {resource} pressure file does not exist.")
            psi_data[resource] = None

    return psi_data

def cpu_stress(duration=30):
    """Induce CPU stress by running multiple CPU-intensive processes."""
    print("Inducing CPU stress...")
    num_processes = multiprocessing.cpu_count()  # One process per core

    def cpu_intensive_task():
        while True:
            pass  # Infinite loop that uses CPU

    processes = []
    for _ in range(num_processes):
        p = multiprocessing.Process(target=cpu_intensive_task)
        p.start()
        processes.append(p)

    time.sleep(duration)  # Let it run for the specified duration

    # Terminate all processes after stress
    for p in processes:
        p.terminate()
        p.join()

    print(f"CPU stress induced for {duration} seconds.")

def memory_stress(duration=30):
    """Induce memory stress by allocating large objects."""
    print("Inducing memory stress...")
    large_list = []

    # Keep allocating memory to create memory pressure
    start_time = time.time()
    while time.time() - start_time < duration:
        large_list.append([random.random() for _ in range(10**6)])  # Each list item is a large list

    print(f"Memory stress induced for {duration} seconds.")

def io_stress(filename="/tmp/io_stress_test.txt", duration=30):
    """Induce I/O stress by writing and reading from a file."""
    print("Inducing I/O stress...")

    try:
        # Write a large file first
        with open(filename, 'w') as f:
            for _ in range(10**6):  # Write 1 million lines of random data
                f.write(''.join(random.choices(string.ascii_letters, k=100)) + "\n")
        print(f"File written successfully: {filename}")

        # Read and write repeatedly to the file
        start_time = time.time()
        while time.time() - start_time < duration:
            with open(filename, 'r') as f:
                data = f.readlines()
            with open(filename, 'a') as f:
                f.writelines(data)  # Rewriting to induce further I/O
        print(f"I/O stress induced for {duration} seconds.")

        # Clean up the file after testing
        os.remove(filename)
        print(f"File removed successfully: {filename}")

    except OSError as e:
        print(f"Error occurred during I/O stress test: {str(e)}")
        print(f"File path: {filename}")

def stress_test_and_collect_psi():
    """Run stress tests and collect PSI data at intervals."""
    # Duration for stress test in seconds
    duration = 30

    print("Starting stress test and PSI data collection...")

    # Collect PSI data before stress
    print("Collecting PSI data before stress test...")
    psi_before = read_psi_info()

    # Run stress tests in parallel
    tests = []                                                                                                                       
                                                                                                                                     
    cpu = multiprocessing.Process(target=cpu_stress, args=(duration,))                                                               
    mem = multiprocessing.Process(target=memory_stress, args=(duration,))                                                            
    io = multiprocessing.Process(target=io_stress, args=(duration,))                                                                 
                                                                                                                                     
    tests.append(cpu)                                                                                                                
    tests.append(mem)                                                                                                                
    tests.append(io)                                                                                                                 
                                                                                                                                     
    for test in tests:                                                                                                               
        test.start()                                                                                                                 
        test.join()  

    # Collect PSI data after stress
    print("Collecting PSI data after stress test...")
    psi_after = read_psi_info()

    print(f"PSI data before stress: {psi_before}")
    print(f"PSI data after stress: {psi_after}")
    
    # Plot PSI data and save to file
    save_psi_graphs(psi_before, psi_after)

def save_psi_graphs(psi_before, psi_after):
    """Plot the PSI data before and after the stress tests and save to file."""
    # Plotting CPU data
    if psi_before['cpu'] and psi_after['cpu']:
        labels = ['avg10', 'avg60', 'avg300']
        before_values = [psi_before['cpu'].get(label, 0) for label in labels]
        after_values = [psi_after['cpu'].get(label, 0) for label in labels]
        
        print(f"CPU Data (before): {before_values}")
        print(f"CPU Data (after): {after_values}")

        plt.figure(figsize=(10, 6))
        plt.bar(labels, before_values, alpha=0.6, label='Before Stress', color='blue')
        plt.bar(labels, after_values, alpha=0.6, label='After Stress', color='red')
        plt.title('CPU Pressure Stall Information')
        plt.ylabel('Pressure (%)')
        plt.legend()
        plt.savefig('psi_graph_cpu.png')  # Save graph to file
        plt.clf()  # Clear the current figure

    # Plotting Memory data
    if psi_before['memory'] and psi_after['memory']:
        labels = ['avg10', 'avg60', 'avg300']
        before_values = [psi_before['memory'].get(label, 0) for label in labels]
        after_values = [psi_after['memory'].get(label, 0) for label in labels]
        
        print(f"Memory Data (before): {before_values}")
        print(f"Memory Data (after): {after_values}")

        plt.figure(figsize=(10, 6))
        plt.bar(labels, before_values, alpha=0.6, label='Before Stress', color='blue')
        plt.bar(labels, after_values, alpha=0.6, label='After Stress', color='red')
        plt.title('Memory Pressure Stall Information')
        plt.ylabel('Pressure (%)')
        plt.legend()
        plt.savefig('psi_graph_memory.png')  # Save graph to file
        plt.clf()  # Clear the current figure

    # Plotting I/O data
    if psi_before['io'] and psi_after['io']:
        labels = ['avg10', 'avg60', 'avg300']
        before_values = [psi_before['io'].get(label, 0) for label in labels]
        after_values = [psi_after['io'].get(label, 0) for label in labels]
        
        print(f"I/O Data (before): {before_values}")
        print(f"I/O Data (after): {after_values}")

        plt.figure(figsize=(10, 6))
        plt.bar(labels, before_values, alpha=0.6, label='Before Stress', color='blue')
        plt.bar(labels, after_values, alpha=0.6, label='After Stress', color='red')
        plt.title('I/O Pressure Stall Information')
        plt.ylabel('Pressure (%)')
        plt.legend()
        plt.savefig('psi_graph_io.png')  # Save graph to file
        plt.clf()  # Clear the current figure

    print("Graphs saved as 'psi_graph_cpu.png', 'psi_graph_memory.png', and 'psi_graph_io.png'.")

if __name__ == '__main__':
    stress_test_and_collect_psi()

