import time
import multiprocessing
import importlib
import json

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
