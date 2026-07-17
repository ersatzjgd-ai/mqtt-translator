import paho.mqtt.client as mqtt
import requests
import time

# Use Railway's internal network names!
# Replace 'find3-mqtt-broker' with the exact name of your Mosquitto service on Railway
MQTT_BROKER = "find3-mqtt-broker" 
MQTT_PORT = 1883 # Internal port, no proxy needed!
MQTT_TOPIC = "kaverigm/passive"

# Replace 'find3' with the exact name of your FIND3 service on Railway
FIND3_HTTP_URL = "http://find3-production:8003/passive"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("SUCCESS: Connected to internal Mosquitto Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Listening for JSON on {MQTT_TOPIC}...")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Caught ESP32 payload: {payload}")
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(FIND3_HTTP_URL, data=payload, headers=headers)
        
        print(f"FIND3 Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Translation Error: {e}")

client = mqtt.Client()

# IF you set a username/password on your Mosquitto broker, uncomment and fill in this line:
client.username_pw_set("kaverigm", "70eix") 

client.on_connect = on_connect
client.on_message = on_message

# Keep trying to connect if Mosquitto is still booting up
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        print(f"Waiting for Mosquitto to come online... ({e})")
        time.sleep(5)

client.loop_forever()
