#!/bin/bash
# MQTT Dashboard Installation and Service Setup Script
# This script automates the installation of the MQTT Dashboard with Simulator as a system service

# Exit on error
set -e

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root or using sudo${NC}"
  exit 1
fi

# Welcome message
echo -e "${GREEN}=== MQTT Dashboard Installation Script ===${NC}"
echo "This script will install the MQTT Dashboard with Simulator as a system service."
echo ""

# Get installation directory
DEFAULT_INSTALL_DIR="/opt/mqtt-dashboard"
read -p "Installation directory [$DEFAULT_INSTALL_DIR]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-$DEFAULT_INSTALL_DIR}

# Get port number
DEFAULT_PORT=8501
read -p "Streamlit port number [$DEFAULT_PORT]: " PORT
PORT=${PORT:-$DEFAULT_PORT}

# Create service user
echo -e "\n${YELLOW}Creating service user...${NC}"
adduser mqtt-dashboard --system --group --disabled-password || true
echo -e "${GREEN}Service user created: mqtt-dashboard${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing system dependencies...${NC}"
apt update
apt install -y python3-pip python3-venv
echo -e "${GREEN}System dependencies installed${NC}"

# Create installation directory
echo -e "\n${YELLOW}Setting up application directory...${NC}"
mkdir -p $INSTALL_DIR
# Get current script directory
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Copy application file
echo -e "${YELLOW}Copying application files...${NC}"
cp "$SCRIPT_DIR/mqtt_dashboard.py" $INSTALL_DIR/
chown -R mqtt-dashboard:mqtt-dashboard $INSTALL_DIR
echo -e "${GREEN}Application files copied to $INSTALL_DIR${NC}"

# Create virtual environment and install Python dependencies
echo -e "\n${YELLOW}Setting up Python virtual environment...${NC}"
cd $INSTALL_DIR
sudo -u mqtt-dashboard python3 -m venv venv
sudo -u mqtt-dashboard ./venv/bin/pip install streamlit paho-mqtt pandas
echo -e "${GREEN}Python dependencies installed${NC}"

# Create systemd service file
echo -e "\n${YELLOW}Creating systemd service...${NC}"
cat > /etc/systemd/system/mqtt-dashboard.service << EOF
[Unit]
Description=MQTT Dashboard with Simulator
After=network.target

[Service]
User=mqtt-dashboard
Group=mqtt-dashboard
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/streamlit run mqtt_dashboard.py --server.address=0.0.0.0 --server.port=$PORT --server.headless=true
Restart=on-failure
RestartSec=5
SyslogIdentifier=mqtt-dashboard

# Security enhancements
ProtectSystem=full
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo -e "${YELLOW}Enabling and starting service...${NC}"
systemctl daemon-reload
systemctl enable mqtt-dashboard.service
systemctl start mqtt-dashboard.service

# Check service status
echo -e "\n${YELLOW}Checking service status...${NC}"
systemctl status mqtt-dashboard.service

# Ask about firewall
echo -e "\n${YELLOW}Firewall configuration:${NC}"
read -p "Open port $PORT in firewall? (y/n): " OPEN_FIREWALL
if [[ $OPEN_FIREWALL == "y" || $OPEN_FIREWALL == "Y" ]]; then
  if command -v ufw &> /dev/null; then
    ufw allow $PORT/tcp
    echo -e "${GREEN}Port $PORT opened in firewall${NC}"
  else
    echo -e "${YELLOW}UFW firewall not detected. Please manually configure your firewall if needed.${NC}"
  fi
fi

# Installation complete
echo -e "\n${GREEN}=== Installation Complete ===${NC}"
echo -e "MQTT Dashboard has been installed and started as a service."
echo -e "You can access it at: http://$(hostname -I | awk '{print $1}'):$PORT"
echo -e "\nService management commands:"
echo -e "  ${YELLOW}sudo systemctl start mqtt-dashboard.service${NC} - Start the service"
echo -e "  ${YELLOW}sudo systemctl stop mqtt-dashboard.service${NC} - Stop the service"
echo -e "  ${YELLOW}sudo systemctl restart mqtt-dashboard.service${NC} - Restart the service"
echo -e "  ${YELLOW}sudo systemctl status mqtt-dashboard.service${NC} - Check service status"
echo -e "  ${YELLOW}sudo journalctl -u mqtt-dashboard.service -f${NC} - View service logs"
echo -e "\nFor more details, refer to the README.md and service setup guide."