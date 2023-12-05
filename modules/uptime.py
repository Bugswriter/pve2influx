import subprocess
import re
import socket

def get_system_uptime_seconds():
    try:
        uptime_output = subprocess.check_output(['uptime']).decode('utf-8').strip()
        uptime_match = re.search(r"up(?:\s+)?((\d+) days?,)?(?:\s+)?(\d+):(\d+)", uptime_output)

        if uptime_match:
            # Corrected line: Convert numeric day value to integer
            days = int(uptime_match.group(2)) if uptime_match.group(2) else 0
            hours, minutes = map(int, uptime_match.group(3, 4))

            uptime_seconds = days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60

            return uptime_seconds
        else:
            raise ValueError("Unable to parse uptime information")

    except Exception as e:
        print(f"Error: {e}")
        return None

def collect_data():
	hostname = socket.gethostname()
	uptime_seconds = get_system_uptime_seconds()
	return {
		"host": hostname,
		"uptime": uptime_seconds
	}

if __name__=="__main__":
	print(collect_data())
