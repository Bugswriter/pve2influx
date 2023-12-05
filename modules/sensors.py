import subprocess
import re

def parse_sensors_output(output):
    sensors_data = {}

    current_adapter = None
    current_core = None

    for line in output.split('\n'):
        if line.strip():
            if 'Adapter' in line:
                current_adapter = re.search(r'Adapter: (.+)', line).group(1)
            elif 'temp' in line or 'Sensor' in line or 'Core' in line:
                parts = re.split(r'\s*:\s*', line)
                
                # Check if parts has the expected number of elements
                if len(parts) == 2:
                    key = parts[0]
                    value = re.search(r'([+-]?\d+\.\d+)', parts[1])

                    if value:
                        if 'Core' in key:
                            current_core = re.search(r'Core (\d+)', key).group(1)
                            full_key = f"{current_adapter}_Core{current_core}_{key.replace(' ', '_')}"
                        else:
                            full_key = f"{current_adapter}_{key.replace(' ', '_')}"
                        
                        sensors_data[full_key] = float(value.group(1))

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
        print(sensors_data)
    else:
        print("Failed to retrieve sensors data.")

