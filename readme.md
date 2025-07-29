# MQTT Dashboard

**Python/Streamlit-based real-time MQTT monitoring and simulation tool for educational IoT projects**

A comprehensive MQTT dashboard built with Python and Streamlit that provides real-time sensor data monitoring and message simulation capabilities. Originally developed to complement the SQL Simulator for a complete IoT data analysis educational experience.

## 🎯 Purpose

This tool provides a complete MQTT ecosystem for educational IoT projects by offering:
- **Real-time MQTT monitoring** - Live dashboard for incoming sensor messages
- **Message simulation** - Generate realistic IoT sensor data for testing and education
- **Educational focus** - Simple interface designed for students learning IoT concepts
- **Data persistence** - Store and analyze received messages locally
- **No complex setup** - Browser-based interface with minimal configuration

## ✨ Features

### Real-time MQTT Dashboard
- **Live message monitoring** - Real-time display of incoming MQTT messages
- **Device management** - Filter and organize data by device and sensor type
- **Data visualization** - Tabular display with latest sensor values
- **Message history** - Store up to 1,000 recent messages with timestamps
- **Connection status** - Clear indication of broker connection health
- **Auto-refresh** - Configurable data polling with manual refresh option

### MQTT Message Simulator
- **Multiple sensor types** - Temperature, humidity, pressure, light, motion sensors
- **Realistic data generation** - Random value generation within sensor-appropriate ranges
- **Custom message creation** - Build messages with custom fields and formats
- **Batch simulation** - Send multiple messages with configurable intervals
- **Message variation** - Add realistic noise and variation to simulated data
- **Real-time publishing** - Immediate message publication to any MQTT topic

### Educational Features
- **Simple configuration** - Minimal setup required for classroom use
- **Visual feedback** - Clear status indicators and error messages
- **Data export capability** - View and analyze collected data
- **Multiple broker support** - Connect to local or remote MQTT brokers
- **Authentication support** - Username/password authentication for secure brokers

## 🏗️ Architecture

```
MQTT Dashboard
├── mqtt_dashboard.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
└── README.md                # This file

Tech Stack:
├── Streamlit                # Web application framework
├── Paho MQTT                # MQTT client library
├── Pandas                   # Data manipulation and display
├── Python Threading         # Async message handling
└── JSON                     # Message parsing and formatting

MQTT Flow:
┌─────────────┐    MQTT     ┌─────────────┐    Streamlit    ┌─────────────┐
│   Sensors   │ ──────────► │    Broker   │ ──────────────► │  Dashboard  │
│  (Physical/ │             │ (Mosquitto/ │                 │  (Browser)  │
│ Simulated)  │             │   Cloud)    │                 │             │
└─────────────┘             └─────────────┘                 └─────────────┘
                                    ▲                               │
                                    │          MQTT Publish         │
                                    └───────────────────────────────┘
                                         Message Simulator
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- MQTT broker (local or remote)
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/jan-milacek/mqtt_dashboard.git
cd mqtt_dashboard
```

2. Install required dependencies:
```bash
pip install streamlit paho-mqtt pandas
```

### Quick Start

#### Run the MQTT Dashboard
```bash
streamlit run mqtt_dashboard.py
```
- Streamlit will automatically open your browser to `http://localhost:8501`
- Configure MQTT broker settings in the sidebar
- Start monitoring real-time sensor data

#### MQTT Broker Setup Options

**Option 1: Local Mosquitto Broker**
```bash
# Install Mosquitto (Ubuntu/Debian)
sudo apt update
sudo apt install mosquitto mosquitto-clients

# Start the broker
sudo systemctl start mosquitto

# Test with dashboard
# Broker: localhost, Port: 1883, Topic: sensors/#
```

**Option 2: Cloud MQTT Broker**
```bash
# Use public test brokers (for education only)
# Broker: test.mosquitto.org, Port: 1883
# Broker: broker.hivemq.com, Port: 1883
```

**Option 3: Docker Mosquitto**
```bash
# Run Mosquitto in Docker
docker run -it -p 1883:1883 eclipse-mosquitto

# Configure dashboard
# Broker: localhost, Port: 1883, Topic: sensors/#
```

## 📊 Usage Examples

### Basic Sensor Monitoring
1. **Connect to broker** - Enter broker details in sidebar
2. **Set topic pattern** - Use `sensors/#` to monitor all sensor topics
3. **Start monitoring** - Click "Connect" to begin receiving messages
4. **View real-time data** - Messages appear instantly in the dashboard

### Message Simulation for Education
1. **Connect to broker** - Ensure MQTT connection is established
2. **Select sensor type** - Choose from temperature, humidity, pressure, etc.
3. **Configure values** - Set realistic ranges or specific values
4. **Send test messages** - Generate individual messages or continuous streams
5. **Monitor in dashboard** - Watch simulated data appear in real-time

### Example Message Formats

**Temperature Sensor**
```json
{
  "device": "device001",
  "sensor": "temperature",
  "sensor_value": 22.5,
  "timestamp": "2024-01-15 10:30:00",
  "battery_level": 85,
  "unit": "celsius"
}
```

**Motion Sensor**
```json
{
  "device": "security_cam_01",
  "sensor": "motion",
  "sensor_value": true,
  "timestamp": "2024-01-15 10:30:00",
  "location": "front_door"
}
```

**Multi-sensor Device**
```json
{
  "device": "weather_station",
  "sensor": "environmental",
  "temperature": 23.1,
  "humidity": 45.2,
  "pressure": 1013.25,
  "timestamp": "2024-01-15 10:30:00"
}
```

## 🎓 Educational Implementation

### Course Integration
This MQTT dashboard complements the SQL Simulator for comprehensive IoT education:

**Week 1-3: IoT Fundamentals**
- Understanding MQTT protocol and pub/sub messaging
- Setting up local MQTT brokers
- Creating and monitoring basic sensor messages

**Week 4-6: Data Collection**
- Simulating realistic sensor scenarios
- Building message schemas for different sensor types
- Understanding data persistence and storage

**Week 7-9: Analysis Pipeline**
- Export MQTT data to CSV format
- Import collected data into SQL Simulator
- Perform analytics on real-time IoT datasets

### Learning Outcomes
Students completing MQTT dashboard exercises can:
- **Understand IoT communication protocols** and message-based architectures
- **Set up and configure MQTT brokers** for device communication
- **Design realistic sensor data schemas** appropriate for different use cases
- **Simulate IoT environments** for testing and development
- **Monitor real-time data streams** and identify data quality issues
- **Bridge IoT data collection with analytical tools** like SQL databases

## 🛠️ Technical Details

### MQTT Features
- **Protocol support** - MQTT v3.1.1 with TCP transport
- **Topic patterns** - Wildcard subscriptions (sensors/#, devices/+/status)
- **QoS levels** - Configurable quality of service for reliable delivery
- **Authentication** - Username/password authentication support
- **Connection management** - Auto-reconnection and error handling

### Message Processing
- **Real-time polling** - Non-blocking message retrieval
- **JSON parsing** - Automatic message parsing with error handling
- **Data buffering** - In-memory storage of recent messages (1,000 message limit)
- **Timestamp tracking** - Automatic receipt timestamps for all messages
- **Device filtering** - Filter messages by device ID or sensor type

### Simulation Capabilities
- **Sensor type templates** - Pre-configured ranges for common sensor types
- **Random value generation** - Realistic data with configurable variation
- **Batch processing** - Send multiple messages with time intervals
- **Custom message structure** - Add arbitrary fields to simulated messages
- **Continuous simulation** - Long-running data generation for testing

### Performance Characteristics
- **Low latency** - Messages appear in dashboard within 100ms
- **Memory efficient** - Limited message buffer prevents memory issues
- **Concurrent handling** - Multiple devices and sensors supported
- **Browser-based** - No local client installation required

## 🤝 Contributing

This project was created for educational IoT development and welcomes contributions:

### Areas for Contribution
- **Additional sensor types** - More realistic sensor simulation templates
- **Data visualization** - Charts and graphs for sensor data trends
- **Export functionality** - Direct CSV export and database integration
- **Broker management** - Built-in broker setup and configuration tools
- **Advanced filtering** - Complex topic filtering and data processing
- **Mobile responsiveness** - Improved mobile device support

### Development Setup
1. Fork the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run application: `streamlit run mqtt_dashboard.py`
6. Test with local MQTT broker or public test brokers

## 📝 Dependencies

```
streamlit>=1.28.0
paho-mqtt>=1.6.1
pandas>=1.5.0
```

## 🔧 Configuration Options

### Broker Configuration
- **Hostname/IP** - Local (localhost, 127.0.0.1) or remote broker addresses
- **Port** - Standard MQTT port (1883) or custom ports
- **Topic patterns** - Flexible subscription patterns with wildcards
- **Authentication** - Optional username/password for secure brokers

### Dashboard Settings
- **Auto-refresh interval** - Configurable polling frequency
- **Data retention** - Message buffer size and retention policies
- **Display filters** - Device and sensor type filtering
- **Message format** - JSON parsing and display options

### Simulation Parameters
- **Sensor ranges** - Realistic value ranges for different sensor types
- **Timing control** - Message intervals and batch sizes
- **Data variation** - Random noise and realistic sensor behavior
- **Custom fields** - Additional metadata and device information

## 📞 Support & Troubleshooting

### Common Issues

**Connection Problems**
```bash
# Check if broker is running
mosquitto_sub -h localhost -t test/topic

# Test with public broker
# Broker: test.mosquitto.org, Port: 1883
```

**Message Not Appearing**
- Verify topic subscription patterns match published topics
- Check JSON format of simulated messages
- Ensure broker connection is stable

**Performance Issues**
- Reduce message buffer size for lower memory usage
- Use specific topic patterns instead of broad wildcards
- Clear data periodically during long monitoring sessions

### Educational Support
For questions about classroom implementation:
- Create an issue in this repository
- Contact: jan.milacek@gmail.com
- Check documentation for configuration examples

## 🔗 Related Projects

- [SQL Simulator](../SQL_simulator) - Companion tool for analyzing collected IoT data
- [Course Materials](../course-materials) - Complete IoT education curriculum

## 📜 License

MIT License - Feel free to use, modify, and distribute for educational purposes.

## 🎯 Real-World Applications

### Educational Scenarios
- **Smart building monitoring** - Temperature, humidity, and occupancy sensors
- **Environmental monitoring** - Weather stations and air quality measurements
- **Industrial IoT** - Machine monitoring and predictive maintenance data
- **Agriculture** - Soil moisture, temperature, and light sensors
- **Home automation** - Security, energy, and comfort monitoring systems

### Professional Development
- **IoT prototyping** - Rapid testing of sensor configurations
- **Data pipeline testing** - Validate data collection before production deployment
- **System integration** - Test MQTT integration with databases and analytics tools
- **Training environments** - Safe learning environment for IoT development skills

---

**Built with ❤️ for IoT education**

*This dashboard demonstrates that complex IoT systems can be made accessible through intuitive interfaces and practical learning experiences. The combination of real-time monitoring with realistic data simulation creates a powerful educational tool for understanding modern IoT architectures.*
