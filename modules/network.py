import psutil
from time import sleep

def get_network_data(interface):
    stats_before = psutil.net_io_counters(pernic=True)[interface]
    sleep(5)  # Adjust the sleep duration as needed
    stats_after = psutil.net_io_counters(pernic=True)[interface]

    receive_bytes = stats_after.bytes_recv - stats_before.bytes_recv
    transmit_bytes = stats_after.bytes_sent - stats_before.bytes_sent

    return receive_bytes, transmit_bytes

def main():
    network_interface = "enp6s0"
    interval_seconds = 5

    try:
        while True:
            receive_bytes, transmit_bytes = get_network_data(network_interface)

            print(f"Network Interface: {network_interface}")
            print(f"Received Data: {receive_bytes} bytes")
            print(f"Transmitted Data: {transmit_bytes} bytes")
            print("=" * 30)

            sleep(interval_seconds)

    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
