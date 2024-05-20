import psutil
import time
import json
import requests
from datetime import datetime

def monitor_high_resource_usage():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    high_resource_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'cmdline']):
        try:
            memory_usage_mb = proc.info['memory_info'].rss / 1024**2
            full_command = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''

            if proc.info['cpu_percent'] > 100 or memory_usage_mb > 1024:
                process_info = {
                    "time": current_time,
                    "pid": proc.info['pid'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_usage_mb": memory_usage_mb,
                    "name": proc.info['name'],
                    "cmdline": full_command
                }
                high_resource_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if high_resource_processes:
        data = {
            "timestamp": current_time,
            "high_resource_processes": high_resource_processes
        }
        try:
            response = requests.post("http://host.docker.internal:8111/notify_1", json=data)
            print(response)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send data: {e}")

# Run the monitoring function every minute
while True:
    monitor_high_resource_usage()
    time.sleep(60)
