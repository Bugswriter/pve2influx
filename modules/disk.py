import os
import socket
import subprocess
import json

def get_smartctl_data():
    disk_path = os.getenv("DISK_PATH")

    if disk_path is None:
        print("DISK_PATH environment variable is not set.")
        return None

    command_output = subprocess.check_output(['smartctl', '-j', '-a', disk_path]).decode('utf-8')

    # Parse JSON output
    smart_data = json.loads(command_output)

    # Extract relevant values from the JSON data
    hostname = socket.gethostname()
    temperature = smart_data.get('temperature', {}).get('current', 0)
    available_spare = smart_data.get('nvme_smart_health_information_log', {}).get('available_spare', 0)
    percentage_used = smart_data.get('nvme_smart_health_information_log', {}).get('percentage_used', 0)
    data_units_read = smart_data.get('nvme_smart_health_information_log', {}).get('data_units_read', 0)
    data_units_written = smart_data.get('nvme_smart_health_information_log', {}).get('data_units_written', 0)
    host_read_commands = smart_data.get('nvme_smart_health_information_log', {}).get('host_reads', 0)
    host_write_commands = smart_data.get('nvme_smart_health_information_log', {}).get('host_writes', 0)
    power_cycles = smart_data.get('nvme_smart_health_information_log', {}).get('power_cycles', 0)
    power_on_hours = smart_data.get('nvme_smart_health_information_log', {}).get('power_on_hours', 0)
    unsafe_shutdowns = smart_data.get('nvme_smart_health_information_log', {}).get('unsafe_shutdowns', 0)
    media_and_data_integrity_errors = smart_data.get('nvme_smart_health_information_log', {}).get('media_errors', 0)

    return {
        "host": hostname,
        "temperature": int(temperature),
        "available_spare": int(available_spare),
        "wearout": int(percentage_used),
        "data_units_read": int(data_units_read),
        "data_units_written": int(data_units_written),
        "host_read_commands": int(host_read_commands),
        "host_write_commands": int(host_write_commands),
        "power_cycles": int(power_cycles),
        "power_on_hours": int(power_on_hours),
        "unsafe_shutdowns": int(unsafe_shutdowns),
        "media_and_data_integrity_errors": int(media_and_data_integrity_errors)
    }

def collect_data():
    return get_smartctl_data()
