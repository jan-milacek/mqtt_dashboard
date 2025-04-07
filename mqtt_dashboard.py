import streamlit as st
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
import json
import time
import pandas as pd
from datetime import datetime
import threading
import queue
import random

# Set page configuration
st.set_page_config(
    page_title="MQTT Sensor Dashboard",
    page_icon="📊",
    layout="wide"
)

# Configure MQTT client in a way that works better with Streamlit
class MQTTManager:
    def __init__(self):
        self.client = None
        self.connected = False
        self.message_buffer = []
        self.error_message = None
        self.broker = None
        self.port = None
        self.username = None
        self.password = None
        
    def connect(self, broker, port, topic, username=None, password=None):
        """Connect to MQTT broker using non-threaded approach"""
        
        # Disconnect existing client if any
        self.disconnect()
        
        # Reset state
        self.connected = False
        self.error_message = None
        
        try:
            # Store connection info for publishing
            self.broker = broker
            self.port = port
            self.username = username
            self.password = password
            
            # Create client with unique ID and disable threading issues
            client_id = f"streamlit-{int(time.time())}"
            self.client = mqtt.Client(client_id=client_id, 
                                     protocol=mqtt.MQTTv311,
                                     transport="tcp")
            
            # Setup callbacks - keeping these very minimal
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    # Successfully connected, but don't modify Streamlit state here
                    pass
                
            def on_message(client, userdata, msg):
                try:
                    # Just append to our local buffer, don't touch Streamlit state
                    payload = json.loads(msg.payload.decode())
                    self.message_buffer.append(payload)
                except:
                    # Silently ignore message parsing errors
                    pass
                    
            self.client.on_connect = on_connect
            self.client.on_message = on_message
            
            # Set auth if provided
            if username and password:
                self.client.username_pw_set(username, password)
                
            # Connect - this will block briefly
            self.client.connect(broker, port, keepalive=60)
            
            # Subscribe to topic
            self.client.subscribe(topic)
            
            # Set connected flag
            self.connected = True
            
            return True
            
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def poll_messages(self):
        """Non-blocking way to get messages"""
        if not self.client or not self.connected:
            return []
        
        # Poll for messages (non-blocking) - just use default loop
        self.client.loop(timeout=0.1)
        
        # Get any messages from buffer
        messages = self.message_buffer.copy()
        # Clear buffer
        self.message_buffer = []
        
        return messages
    
    def publish_message(self, topic, payload):
        """Publish a message to a topic"""
        if not self.connected or not self.broker:
            return False, "Not connected to a broker"
        
        try:
            # Create auth dict if credentials provided
            auth = None
            if self.username and self.password:
                auth = {'username': self.username, 'password': self.password}
            
            # Publish message
            mqtt_publish.single(
                topic, 
                payload=json.dumps(payload), 
                hostname=self.broker,
                port=self.port,
                auth=auth if auth else None
            )
            return True, "Message published successfully"
        except Exception as e:
            return False, f"Failed to publish message: {str(e)}"
    
    def disconnect(self):
        """Disconnect from broker"""
        if self.client:
            try:
                self.client.disconnect()
            except:
                pass  # Ignore disconnection errors
            
            self.client = None
            self.connected = False

# Initialize MQTT manager in session state
if 'mqtt_manager' not in st.session_state:
    st.session_state.mqtt_manager = MQTTManager()

# Initialize data store in session state 
if 'data' not in st.session_state:
    st.session_state.data = []

# Title and description
st.title("MQTT Sensor Dashboard")
st.markdown("Simple, reliable MQTT monitoring solution with message simulator")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Dashboard", "Message Simulator"])

# Sidebar for MQTT configuration
with st.sidebar:
    st.header("MQTT Configuration")
    
    # MQTT broker settings with defaults
    mqtt_broker = st.text_input("MQTT Broker", "localhost")
    mqtt_port = st.number_input("MQTT Port", value=1883, min_value=1, max_value=65535)
    mqtt_topic = st.text_input("MQTT Topic", "sensors/#")
    
    # Optional authentication
    with st.expander("Authentication (Optional)"):
        mqtt_username = st.text_input("Username", "")
        mqtt_password = st.text_input("Password", "", type="password")
    
    # Connect/disconnect buttons
    if st.session_state.mqtt_manager.connected:
        if st.button("Disconnect", type="secondary"):
            st.session_state.mqtt_manager.disconnect()
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Connect", type="primary"):
                if st.session_state.mqtt_manager.connect(
                    mqtt_broker, mqtt_port, mqtt_topic, 
                    mqtt_username if mqtt_username else None,
                    mqtt_password if mqtt_password else None
                ):
                    st.success("Connected!")
                    st.rerun()
                else:
                    st.error(f"Connection failed: {st.session_state.mqtt_manager.error_message}")
        
        with col2:
            if st.button("Try 127.0.0.1"):
                if st.session_state.mqtt_manager.connect("127.0.0.1", mqtt_port, mqtt_topic):
                    st.success("Connected!")
                    st.rerun()
    
    # Show connection status
    st.subheader("Connection Status")
    if st.session_state.mqtt_manager.connected:
        st.success(f"Connected to {mqtt_broker}:{mqtt_port}")
        st.info(f"Listening on topic: {mqtt_topic}")
    else:
        st.error("Not connected")
        if st.session_state.mqtt_manager.error_message:
            st.info(f"Error: {st.session_state.mqtt_manager.error_message}")
    
    # Clear data button
    if st.button("Clear Data"):
        st.session_state.data = []
        st.rerun()

# Dashboard tab
with tab1:
    # Poll for messages if connected
    if st.session_state.mqtt_manager.connected:
        try:
            new_messages = st.session_state.mqtt_manager.poll_messages()
            if new_messages:
                # Add timestamp
                for msg in new_messages:
                    if 'received_at' not in msg:
                        msg['received_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Add to our data store
                st.session_state.data.extend(new_messages)
                
                # Keep data store at reasonable size (latest 1000 messages)
                if len(st.session_state.data) > 1000:
                    st.session_state.data = st.session_state.data[-1000:]
        except Exception as e:
            st.error(f"Error polling messages: {str(e)}")
            # Try to disconnect/reconnect on error
            st.session_state.mqtt_manager.disconnect()

    # Create DataFrame from stored data
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        
        # Split display into columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"Sensor Data ({len(df)} messages)")
            st.dataframe(df.sort_values(by='received_at', ascending=False), use_container_width=True)
        
        with col2:
            st.subheader("Device Summary")
            
            # Get unique devices
            if 'device' in df.columns:
                devices = df['device'].unique()
                device_select = st.selectbox("Select Device", ["All"] + list(devices))
                
                # Filter data based on selected device
                if device_select != "All":
                    filtered_df = df[df['device'] == device_select]
                else:
                    filtered_df = df
                
                # Show latest values for each sensor
                if 'sensor' in filtered_df.columns:
                    st.subheader("Latest Sensor Values")
                    latest_sensors = filtered_df.sort_values('received_at', ascending=False).drop_duplicates('sensor')
                    for _, row in latest_sensors.iterrows():
                        sensor_name = row.get('sensor', 'Unknown')
                        sensor_value = row.get('sensor_value', 'N/A')
                        timestamp = row.get('timestamp', row.get('received_at', 'Unknown'))
                        
                        # Display each sensor in a simple way
                        st.metric(
                            label=f"{sensor_name}",
                            value=sensor_value,
                            delta=None
                        )
    else:
        # Empty state
        st.info("No data received yet. Connect to MQTT broker to start receiving messages.")

    # Simple manual refresh button with current time display
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Refresh Data"):
            st.rerun()
        st.write(f"Last refreshed: {datetime.now().strftime('%H:%M:%S')}")

# Message Simulator tab
with tab2:
    st.header("MQTT Message Simulator")
    
    if not st.session_state.mqtt_manager.connected:
        st.warning("Connect to an MQTT broker first to simulate messages")
    else:
        st.success("Connected to MQTT broker - ready to simulate messages")
        
        # Basic message template
        st.subheader("Create Message")
        
        # Topic selection
        sim_topic = st.text_input("Topic", "sensors/test")
        
        # Create columns for form inputs
        col1, col2 = st.columns(2)
        
        with col1:
            # Device and sensor selection
            device_id = st.text_input("Device ID", "device001")
            sensor_type = st.selectbox("Sensor Type", 
                                      ["temperature", "humidity", "pressure", "light", "motion", "custom"])
            
            if sensor_type == "custom":
                sensor_type = st.text_input("Custom Sensor Type", "")
        
        with col2:
            # Message value
            if sensor_type in ["temperature", "humidity", "pressure"]:
                # For numeric sensors, allow random values
                use_random = st.checkbox("Generate Random Value")
                
                if use_random:
                    # Different ranges based on sensor type
                    if sensor_type == "temperature":
                        min_val, max_val = st.slider("Temperature Range (°C)", -20.0, 50.0, (15.0, 25.0))
                        sensor_value = round(random.uniform(min_val, max_val), 1)
                    elif sensor_type == "humidity":
                        min_val, max_val = st.slider("Humidity Range (%)", 0.0, 100.0, (30.0, 70.0))
                        sensor_value = round(random.uniform(min_val, max_val), 1)
                    elif sensor_type == "pressure":
                        min_val, max_val = st.slider("Pressure Range (hPa)", 980.0, 1050.0, (1000.0, 1020.0))
                        sensor_value = round(random.uniform(min_val, max_val), 1)
                    
                    st.info(f"Generated value: {sensor_value}")
                else:
                    # Manual value entry
                    sensor_value = st.number_input("Sensor Value", value=0.0, step=0.1)
            elif sensor_type == "motion":
                # Boolean sensor
                sensor_value = st.selectbox("Motion Detected", [True, False])
            elif sensor_type == "light":
                # Light level (0-100%)
                sensor_value = st.slider("Light Level (%)", 0, 100, 50)
            else:
                # Custom sensor - free text
                sensor_value = st.text_input("Sensor Value", "")
        
        # Advanced message options
        with st.expander("Advanced Message Options"):
            # Additional fields
            include_timestamp = st.checkbox("Include Current Timestamp", True)
            include_battery = st.checkbox("Include Battery Level")
            
            if include_battery:
                battery_level = st.slider("Battery Level (%)", 0, 100, 75)
            
            # Custom fields
            custom_fields = st.text_area("Additional Custom Fields (JSON format)", '{"unit": "celsius"}')
            
        # Preview message
        st.subheader("Message Preview")
        
        # Build message payload
        message = {
            "device": device_id,
            "sensor": sensor_type,
            "sensor_value": sensor_value
        }
        
        # Add optional fields
        if include_timestamp:
            message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if include_battery and 'battery_level' in locals():
            message["battery_level"] = battery_level
        
        # Add custom fields if provided
        try:
            if custom_fields:
                custom_json = json.loads(custom_fields)
                message.update(custom_json)
        except json.JSONDecodeError:
            st.error("Invalid JSON in custom fields")
        
        # Show preview
        st.code(json.dumps(message, indent=2))
        
        # Send button
        if st.button("Send Message", type="primary"):
            success, message_status = st.session_state.mqtt_manager.publish_message(sim_topic, message)
            
            if success:
                st.success(message_status)
                
                # Add message to local data for immediate display
                message_copy = message.copy()
                message_copy["received_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.data.append(message_copy)
                
                # Keep data store at reasonable size
                if len(st.session_state.data) > 1000:
                    st.session_state.data = st.session_state.data[-1000:]
            else:
                st.error(message_status)
        
        # Simulation section for repeated messages
        st.subheader("Simulate Stream of Messages")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_simulate = st.checkbox("Enable Auto-Simulation")
            
            if auto_simulate:
                sim_interval = st.number_input("Interval (seconds)", min_value=1, max_value=60, value=5)
                sim_count = st.number_input("Number of Messages (0 for continuous)", min_value=0, max_value=100, value=10)
                
                # Variation settings
                add_variation = st.checkbox("Add Random Variation to Values")
                
                if add_variation:
                    variation_percent = st.slider("Variation Amount (%)", 1, 50, 10)
        
        with col2:
            if auto_simulate:
                st.info("Auto-simulation will send messages with the configuration from the 'Create Message' section above.")
                st.warning("To stop simulation early, uncheck 'Enable Auto-Simulation'")
                
                if st.button("Start Simulation"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Track how many messages sent
                    sent_count = 0
                    continuing = True
                    
                    while continuing and auto_simulate:
                        # Check if we've reached the desired count
                        if sim_count > 0 and sent_count >= sim_count:
                            break
                        
                        # Create message copy
                        sim_message = message.copy()
                        
                        # Add variation if requested
                        if add_variation and isinstance(sensor_value, (int, float)):
                            variation_amount = sensor_value * (variation_percent / 100)
                            sim_message["sensor_value"] = round(
                                sensor_value + random.uniform(-variation_amount, variation_amount), 
                                1
                            )
                        
                        # Update timestamp if included
                        if include_timestamp:
                            sim_message["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Send message
                        success, _ = st.session_state.mqtt_manager.publish_message(sim_topic, sim_message)
                        
                        if success:
                            sent_count += 1
                            
                            # Add message to local data
                            message_copy = sim_message.copy()
                            message_copy["received_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.data.append(message_copy)
                            
                            # Keep data store reasonable
                            if len(st.session_state.data) > 1000:
                                st.session_state.data = st.session_state.data[-1000:]
                            
                            # Update progress and status
                            if sim_count > 0:
                                progress_bar.progress(sent_count / sim_count)
                                status_text.text(f"Sent {sent_count}/{sim_count} messages")
                            else:
                                status_text.text(f"Sent {sent_count} messages (continuous mode)")
                        
                        # Sleep for interval
                        time.sleep(sim_interval)
                    
                    status_text.text(f"Simulation completed - sent {sent_count} messages")
                    progress_bar.progress(1.0)