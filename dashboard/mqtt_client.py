import paho.mqtt.client as mqtt
#import os
#import django

import json
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
#django.setup()

from dashboard.models import SensorData

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "water/temperature"   # Must match ESP32 topic

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)


    
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print("Received:", payload)

        temperature = float(payload)

        SensorData.objects.create(
            topic=msg.topic,
             value=float(msg.payload.decode())
        
        )

        print("Saved to database!")

    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()