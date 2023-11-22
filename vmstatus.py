import os
from threading import Thread
import inotify.adapters
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

log_file="/var/log/pve/tasks/index"

influx_url = os.getenv("INFLUX_URL")
influx_token = os.getenv("INFLUX_TOKEN")
influx_org = os.getenv("INFLUX_ORG")
influx_bucket = os.getenv("INFLUX_BUCKET")


def write_in_influx(data):
    client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    p = Point("vmstatus").tag("vmid", data['vmid']).field("status", data['status']).field("details", data['details'])
    write_api.write(bucket=influx_bucket, record=p)


def parse_data(log):
	log_parts = log.split(':')

	if log_parts[5] != 'qmstart' and log_parts[5] != 'qmstop':
		return

	log_data = {
		'status': log_parts[5],
		'vmid': log_parts[6],
		'details': log_parts[8].strip()
	}
	write_in_influx(log_data)



def monitor_file(file_path):
    i = inotify.adapters.Inotify()
    i.add_watch(file_path)

    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event

            if "IN_MODIFY" in type_names:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    last_line = lines[-1].strip()
                    t1 = Thread(target=parse_data, args=(last_line,))
                    t1.run()


    finally:
        i.remove_watch(file_path)

monitor_file(log_file)
