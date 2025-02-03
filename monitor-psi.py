import read_psi_info as psi_info
import multiprocessing
import time
import csv
import os

def monitor_psi(path, interval, use_csv):
    while True:
        data = psi_info.read_psi_info()
        timestamp = time.ctime()
        if use_csv:
            with open(path + "/cpu/" + timestamp + ".csv", 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerows(data["cpu"])
            with open(path + "/memory/" + timestamp + ".csv", 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerows(data["memory"])
            with open(path + "/io/" + timestamp + ".csv", 'a') as file:
                csvwriter = csv.writer(file)
                csvwriter.writerows(data["io"])
        else:
            pass
        time.sleep(interval)

def start_monitoring(path='./psi_data', interval=10, use_csv=False):
    if use_csv:
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path + "/cpu"):
            os.mkdir(path + "/cpu")
        if not os.path.exists(path + "/memory"):
            os.mkdir(path + "/memory")
        if not os.path.exists(path + "/io"):
            os.mkdir(path + "/io")
    monitor = multiprocessing.Process(target=monitor_psi, args=(path, interval, csv,))
    monitor.start()
    return monitor

def stop_monitoring(monitor):
    monitor.terminate()
    monitor.join()
