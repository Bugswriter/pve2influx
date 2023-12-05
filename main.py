import os
import time
import multiprocessing
import importlib
import json

from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()


def create_influxdb_point(measurement, data):
    point = influxdb_client.Point(measurement)
    for key, value in data.items():
        if key == 'host':
            point = point.tag(key, value)
        else:
            point = point.field(key, value)

    return point

def get_influx_write_api():
	influx_url = os.getenv("INFLUX_URL")
	influx_token = os.getenv("INFLUX_TOKEN")
	influx_org = os.getenv("INFLUX_ORG")
	influx_bucket = os.getenv("INFLUX_BUCKET")
	
	client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
	write_api = client.write_api(write_options=SYNCHRONOUS)
	return write_api


def run_module(module_name, interval_seconds=None):
	try:
		module = importlib.import_module(f"modules.{module_name}")
		process = multiprocessing.Process(
			target=module.collect_and_send_metrics, args=(interval_seconds,))
			
		process.start()
		return process

	except Exception as e:
		print(f"Error running module '{module_name}': {e}")

def load_module_config(module_config_file):
	try:
		with open(f"config/{module_config_file}", 'r') as f:
			return json.load(f)
	except Exception as e:
		print(f"Error loading config module: {e}")

def check_processes(processes):
    for process in processes:
        if process.is_alive():
            continue
        else:
            print(f"Process {process.name} has terminated unexpectedly!")

def main():
	module_config_file = "modules_config.json"
	module_config = load_module_config(module_config_file)
	running_modules = []

	for module in module_config.get('modules', []):
		module_name = module.get('name')
		interval_seconds = module.get('interval_seconds')
		process = run_module(module_name, interval_seconds)
			
		if process:
			running_modules.append(process)

	print("process manager is started")
	while True:
		check_processes(running_modules)
		time.sleep(10)

if __name__ == "__main__":
	main()
