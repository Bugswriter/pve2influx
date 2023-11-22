# System Monitoring Scripts

This repository contains Python scripts for gathering host machine information and sending it to InfluxDB. The scripts cover various aspects, including disk statistics, KVM virtual machine status, and sensor readings.

## Prerequisites

Make sure you have the following installed on your system:

- Python 3.x
- InfluxDB
- [InfluxDB Python Client](https://github.com/influxdata/influxdb-client-python)

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/bugswriter/pve2influx.git
    cd pve2influx
    ```

2. Set up a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your InfluxDB configuration by creating a `.env` file with the following variables:

    ```env
    INFLUX_URL="https://your-influxdb-url:8086"
    INFLUX_TOKEN="your-influxdb-token"
    INFLUX_ORG="your-influxdb-organization"
    INFLUX_BUCKET="your-influxdb-bucket"
    ```

5. Run the desired scripts:

    ```bash
    python disk.py
    python vmstatus.py
    python sensors.py
    # Add more scripts as needed
    ```

## Scripts

### 1. disk.py

This script retrieves disk statistics and sends them to InfluxDB.

### 2. vmstatus.py

Monitors the status of KVM virtual machines and logs the information to InfluxDB.

### 3. sensors.py

Gathers sensor readings from the host machine and stores them in InfluxDB.

## Contributing

Feel free to contribute by opening issues, suggesting improvements, or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

