import os
import time
import json
import importlib
import schedule
from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

influx_url = os.getenv("INFLUX_URL")
influx_token = os.getenv("INFLUX_TOKEN")
influx_org = os.getenv("INFLUX_ORG")
influx_bucket = os.getenv("INFLUX_BUCKET")

client = influxdb_client.InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def create_influxdb_point(measurement, data):
    point = influxdb_client.Point(measurement)
    for key, value in data.items():
        if key == 'host':
            # hotfix for dot in hostname
            point = point.tag(key, value.split('.')[0])
        else:
            point = point.field(key, value)

    return point

def load_config():
    with open('config/modules_config.json', 'r') as f:
        config = json.load(f)
    return config.get("modules", [])


def run_module(module_name):
    module = importlib.import_module(f"modules.{module_name}")
    data = module.collect_data()

    if isinstance(data, list):
        # If collect data return multiple records
        for record in data:
            point = create_influxdb_point(module_name, record)
            write_api.write(bucket=influx_bucket, org=influx_org, record=point)
            print(f"writing record for {module_name} finished.")

    else:
        point = create_influxdb_point(module_name, data)
        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print(f"writing record for {module_name} finished.")

def main():
    modules_config = load_config()
    for module_config in modules_config:
        module_name = module_config["name"]
        interval_seconds = module_config.get("interval_seconds", False)

        schedule.every(interval_seconds).seconds.do(
            run_module, module_name=module_name)

    while True:
        schedule.run_pending()
        time.sleep(1)

main()
