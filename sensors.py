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

