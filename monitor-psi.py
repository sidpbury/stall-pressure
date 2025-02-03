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
            with open(path + "/cpu", 'a') as file:
                file.write(timestamp + ":\n")
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["cpu"][1])) + '\n')
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["cpu"][2])) + '\n\n')
            with open(path + "/memory", 'a') as file:
                file.write(timestamp + ":\n")
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["memory"][1])) + '\n')
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["memory"][2])) + '\n\n')
            with open(path + "/io", 'a') as file:
                file.write(timestamp + ":\n")
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["io"][1])) + '\n')
                file.write('\t'.join(map(lambda x: f"{x:.2f}" if type(x) == float else x, data["io"][2])) + '\n\n')
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

monitor = start_monitoring()
time.sleep(20)
stop_monitoring(monitor)
