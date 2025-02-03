import read_psi_info as psi_info
import multiprocessing
import time
import csv
import os

def log_data(path, data, timestamp, resource):
    with open(path + "/" + resource, 'a') as file:
                file.write(timestamp + ":\n")
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data[resource][1])) + '\n')
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data[resource][2])) + '\n\n')

def log_csv(path, data, timestamp, resource):
    with open(path + "/" + resource + "/" + timestamp + ".csv", 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerows(data[resource])

def monitor_psi(path, interval, use_csv):
    while True:
        data = psi_info.read_psi_info()
        timestamp = time.ctime()
        if use_csv:
            log_csv(path, data, timestamp, "cpu")
            log_csv(path, data, timestamp, "memory")
            log_csv(path, data, timestamp, "io")
        else:
            log_data(path, data, timestamp, "cpu")
            log_data(path, data, timestamp, "memory")
            log_data(path, data, timestamp, "io")
        time.sleep(interval)

def start_monitoring(path='./psi_data', interval=10, use_csv=False):
    if not os.path.exists(path):
        os.mkdir(path)
    if use_csv:
        if not os.path.exists(path + "/cpu"):
            os.mkdir(path + "/cpu")
        if not os.path.exists(path + "/memory"):
            os.mkdir(path + "/memory")
        if not os.path.exists(path + "/io"):
            os.mkdir(path + "/io")
    else:
        with open(path + "/cpu", 'a') as file:
            file.write("name\tavg10\tavg60\tavg300\ttotal\n")
        with open(path + "/memory", 'a') as file:
            file.write("name\tavg10\tavg60\tavg300\ttotal\n")
        with open(path + "/io", 'a') as file:
            file.write("name\tavg10\tavg60\tavg300\ttotal\n")

    monitor = multiprocessing.Process(target=monitor_psi, args=(path, interval, use_csv,))
    monitor.start()
    return monitor

def stop_monitoring(monitor):
    monitor.terminate()
    monitor.join()
