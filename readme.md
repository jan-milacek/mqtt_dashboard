# MQTT Dashboard with Simulator

A Streamlit-based web application for monitoring MQTT messages in real-time with built-in message simulation capabilities.

![MQTT Dashboard](mqtt_dashboard_screenshot.png)

## Features

- **Real-time MQTT Message Monitoring**
  - Connect to any MQTT broker
  - Subscribe to specific topics
  - View messages in a sortable data table
  - See device and sensor summaries

- **MQTT Message Simulator**
  - Create custom MQTT messages
  - Generate random sensor values
  - Simulate message streams at defined intervals
  - Add controlled variation to simulated values

- **Easy Configuration**
  - Simple broker connection settings
  - Optional authentication support
  - Persistent connection management
  - Clear, intuitive interface

## Requirements

- Python 3.7+
- Streamlit
- Paho MQTT client
- pandas

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jan-milacek/mqtt_dashboard.git
   cd mqtt_dashboard
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install streamlit paho-mqtt pandas
   ```

## Usage

Run the application using Streamlit:

```bash
streamlit run mqtt_dashboard.py
```

Then open your browser to http://localhost:8501 to access the dashboard.

### Dashboard Tab

The main dashboard displays:
- A data table of all received MQTT messages
- Device summaries and sensor readings
- Connection status information

### Simulator Tab

The simulator allows you to:
- Create custom MQTT messages
- Set device IDs and sensor types
- Generate random or specific sensor values
- Send individual messages or continuous streams
- Add variation to simulated data

## Configuration

Configure the application by setting these parameters in the sidebar:
- MQTT Broker address (default: localhost)
- MQTT Port (default: 1883)
- MQTT Topic to subscribe to (default: sensors/#)
- Optional username and password

## Running as a Service

See the [Service Setup Guide](service-setup.md) for instructions on running the dashboard as a system service.