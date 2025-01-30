import read_psi_info as psi_info
import multiprocessing

def monitor_psi(invterval, data):
    pass

def start_monitoring(interval=10, data=[]):
    monitor = multiprocessing.Process(target=monitor_psi, args=(interval, data,))
    monitor.start()
    return monitor, data

def stop_monitoring(monitor):
    monitor.join()
    monitor.terminate()
