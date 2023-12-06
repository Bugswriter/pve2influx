import time
import os
import socket
from dotenv import load_dotenv
from datetime import datetime
import subprocess
import re
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

def create_influxdb_point(measurement, data):
    point = influxdb_client.Point(measurement)

    # Add tags and fields dynamically from the dictionary
    for key, value in data.items():
        if key == 'host':
            point = point.tag(key, value)
        else:
            point = point.field(key, value)

    return point

def get_smartctl_data():
	disk = os.getenv("DISK_PATH")

	if disk is None:
		print("DISK_PATH environment variable is not set.")
		return None

	command_output = subprocess.check_output(['smartctl', '-a', disk]).decode('utf-8')


	# Extract relevant values from the output using regular expressions
	hostname = socket.gethostname()
	temperature = re.search(r'Temperature:\s+(\d+)\sCelsius', command_output).group(1)
	available_spare = re.search(r'Available Spare:\s+(\d+)%', command_output).group(1)
	percentage_used = re.search(r'Percentage Used:\s+(\d+)%', command_output).group(1)
	data_units_read = re.search(r'Data Units Read:\s+(\d+)', command_output).group(1)
	data_units_written = re.search(r'Data Units Written:\s+(\d+)', command_output).group(1)
	host_read_commands = re.search(r'Host Read Commands:\s+(\d+)', command_output).group(1)
	host_write_commands = re.search(r'Host Write Commands:\s+(\d+)', command_output).group(1)
	power_cycles = re.search(r'Power Cycles:\s+(\d+)', command_output).group(1)
	power_on_hours = re.search(r'Power On Hours:\s+(\d+)', command_output).group(1)
	unsafe_shutdowns = re.search(r'Unsafe Shutdowns:\s+(\d+)', command_output).group(1)
	media_and_data_integrity_errors = re.search(r'Media and Data Integrity Errors:\s+(\d+)', command_output).group(1)

	return {
		"host": hostname,
		"temperature": int(temperature),
		"available_spare": int(available_spare),
		"percentage_used": int(percentage_used),
		"data_units_read": int(data_units_read),
		"data_units_written": int(data_units_written),
		"host_read_commands": int(host_read_commands),
		"host_write_commands": int(host_write_commands),
		"power_cycles": int(power_cycles),
		"power_on_hours": int(power_on_hours),
		"unsafe_shutdowns": int(unsafe_shutdowns),
		"media_and_data_integrity_errors": int(media_and_data_integrity_errors)
	}


def collect_and_send_metrics(interval_seconds):
	influx_url = os.getenv("INFLUX_URL")
	influx_token = os.getenv("INFLUX_TOKEN")
	influx_org = os.getenv("INFLUX_ORG")
	influx_bucket = os.getenv("INFLUX_BUCKET")

	client = influxdb_client.InfluxDBClient(
			 url=influx_url,
			 token=influx_token,
			 org=influx_org
	)

	write_api = client.write_api(write_options=SYNCHRONOUS)


	time.sleep(interval_seconds)
	disk_data = get_smartctl_data()

	point = create_influxdb_point("disk", disk_data)
	write_api.write(bucket=influx_bucket, org=influx_org, record=point)
	current_datetime = datetime.now()
	_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
	print(f"{_datetime} - writing disk module record")
	

def test(interval_seconds):
	while True:
		time.sleep(interval_seconds)
		print(f"{time.time()} - Disk module")

	
if __name__=="__main__":
	collect_and_send_metrics(10)
