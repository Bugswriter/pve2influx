import subprocess

def parse_sensors_output(output):
    sensor_data = {}
    current_adapter = None
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith("Adapter:"):
            current_adapter = line.split(":")[1].strip()
            sensor_data[current_adapter] = {}
        elif current_adapter and ':' in line:
            key_value = line.split(":")
            if len(key_value) >= 2:
                key, value = key_value[0].strip(), ':'.join(key_value[1:]).strip()
                sensor_data[current_adapter][key] = value
    return sensor_data

def get_sensor_info():
    try:
        output = subprocess.check_output(["sensors"], universal_newlines=True, stderr=subprocess.STDOUT)
        return parse_sensors_output(output)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return {"Error": str(e)}

sensor_info = get_sensor_info()
print(sensor_info)

import subprocess
import re

def parse_sensors_output(output):
    sensors_data = {}
    current_adapter = None

    for line in output.split('\n'):
        if line.strip():
            if 'Adapter' in line:
                current_adapter = re.search(r'Adapter: (.+)', line).group(1)
                sensors_data[current_adapter] = {}
            elif 'temp' in line or 'Sensor' in line:
                parts = re.split(r'\s*:\s*', line)
                
                # Check if parts has the expected number of elements
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1]
                    sensors_data[current_adapter][key] = value

    return sensors_data

def get_sensors_data():
    try:
        output = subprocess.check_output(['sensors'], text=True)
        return parse_sensors_output(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    sensors_data = get_sensors_data()

    if sensors_data:
        print("Parsed Sensors Data:")
        print(sensors_data)
    else:
        print("Failed to retrieve sensors data.")

