# Setting Up MQTT Dashboard as an Ubuntu Service

This guide will help you set up the MQTT Dashboard with Simulator as a systemd service on Ubuntu, allowing it to run automatically at system startup and be managed like other system services.

## Prerequisites

- Ubuntu 18.04 or newer
- Python 3.7+ installed
- MQTT Dashboard application installed
- sudo privileges

## Installation Steps

### 1. Create a Dedicated User (Optional but Recommended)

For better security, create a dedicated user to run the service:

```bash
sudo adduser mqtt-dashboard --system --group --disabled-password
```

### 2. Install Required Dependencies

```bash
# Update package lists
sudo apt update

# Install required packages
sudo apt install -y python3-pip python3-venv

# Create a directory for the application (if not already done)
sudo mkdir -p /opt/mqtt-dashboard
```

### 3. Set Up the Application

Copy your application files to the installation directory:

```bash
# Copy application files
sudo cp -r /path/to/your/mqtt_dashboard.py /opt/mqtt-dashboard/
sudo chown -R mqtt-dashboard:mqtt-dashboard /opt/mqtt-dashboard/

# Create virtual environment
cd /opt/mqtt-dashboard
sudo -u mqtt-dashboard python3 -m venv venv
sudo -u mqtt-dashboard ./venv/bin/pip install streamlit paho-mqtt pandas
```

### 4. Create a Service Configuration File

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/mqtt-dashboard.service
```

Add the following content to the file:

```ini
[Unit]
Description=MQTT Dashboard with Simulator
After=network.target

[Service]
User=mqtt-dashboard
Group=mqtt-dashboard
WorkingDirectory=/opt/mqtt-dashboard
ExecStart=/opt/mqtt-dashboard/venv/bin/streamlit run mqtt_dashboard.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
Restart=on-failure
RestartSec=5
SyslogIdentifier=mqtt-dashboard

# Optional security enhancements
ProtectSystem=full
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

Save and close the file (Ctrl+X, then Y, then Enter in nano).

### 5. Enable and Start the Service

```bash
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start at boot
sudo systemctl enable mqtt-dashboard.service

# Start the service
sudo systemctl start mqtt-dashboard.service
```

### 6. Check Service Status

Verify that the service is running correctly:

```bash
sudo systemctl status mqtt-dashboard.service
```

You should see output indicating that the service is active (running).

### 7. Configure Firewall (Optional)

If you're using the UFW firewall and want to access the dashboard from other computers:

```bash
sudo ufw allow 8501/tcp
```

## Service Management Commands

Here are some useful commands for managing your MQTT Dashboard service:

```bash
# Start the service
sudo systemctl start mqtt-dashboard.service

# Stop the service
sudo systemctl stop mqtt-dashboard.service

# Restart the service
sudo systemctl restart mqtt-dashboard.service

# Check service status
sudo systemctl status mqtt-dashboard.service

# View service logs
sudo journalctl -u mqtt-dashboard.service

# View recent logs
sudo journalctl -u mqtt-dashboard.service -n 50

# Follow logs in real-time
sudo journalctl -u mqtt-dashboard.service -f
```

## Updating the Application

To update the application:

1. Stop the service:
   ```bash
   sudo systemctl stop mqtt-dashboard.service
   ```

2. Update the application files:
   ```bash
   sudo cp -r /path/to/new/mqtt_dashboard.py /opt/mqtt-dashboard/
   ```

3. Update dependencies if needed:
   ```bash
   cd /opt/mqtt-dashboard
   sudo -u mqtt-dashboard ./venv/bin/pip install --upgrade streamlit paho-mqtt pandas
   ```

4. Restart the service:
   ```bash
   sudo systemctl start mqtt-dashboard.service
   ```

## Troubleshooting

If you encounter issues:

1. Check the service status:
   ```bash
   sudo systemctl status mqtt-dashboard.service
   ```

2. Check the logs:
   ```bash
   sudo journalctl -u mqtt-dashboard.service -n 100
   ```

3. Common issues include:
   - Port conflicts (change the port in the service file)
   - Permissions issues (ensure proper ownership of files)
   - Missing dependencies (check if all packages are installed)

## Security Considerations

- Consider setting up HTTPS using a reverse proxy like Nginx
- Implement authentication for the Streamlit interface
- Use environment variables for sensitive configuration instead of hardcoding
- Restrict network access to the service if used in production
