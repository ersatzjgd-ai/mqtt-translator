import paho.mqtt.client as mqtt
import requests
import json

# 1. Listen to your external Mosquitto Broker
MQTT_BROKER = "tokaido.proxy.rlwy.net" 
MQTT_PORT = 45223
MQTT_TOPIC = "kaverigm/passive"

# 2. Point to FIND3's INTERNAL HTTP API (Localhost/Docker network)
FIND3_HTTP_URL = "http://localhost:8003/passive" 

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Listening for JSON on {MQTT_TOPIC}...")

def on_message(client, userdata, msg):
    try:
        # Catch the perfect JSON from the ESP32
        payload = msg.payload.decode('utf-8')
        print(f"Caught payload: {payload}")
        
        # Fire it instantly into FIND3 via internal HTTP
        headers = {'Content-Type': 'application/json'}
        response = requests.post(FIND3_HTTP_URL, data=payload, headers=headers)
        
        print(f"FIND3 Response: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"Translation Error: {e}")

client = mqtt.Client()
# client.username_pw_set("kaveri_edge", "SecureLounge2026!") # Add if using auth
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
