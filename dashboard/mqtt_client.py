import paho.mqtt.client as mqtt
#import os
#import django

import json
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
#django.setup()

from dashboard.models import SensorData

BROKER = "broker.emqx.io"
PORT = 1883

#ESP32 Topics
TEMP_TOPIC = "water/temperature"  
PH_TOPIC = "water/ph"
TURBIDITY_TOPIC = "water/turbidity"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

    client.subscribe(TEMP_TOPIC)
    client.subscribe(PH_TOPIC)
    client.subscribe(TURBIDITY_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print("Received:", payload)

        value = float(payload)

        if msg.topic == TEMP_TOPIC:
            SensorData.objects.create(temperature=value)

        elif msg.topic == PH_TOPIC:
            SensorData.objects.create(ph=value)

        elif msg.topic == TURBIDITY_TOPIC:
            SensorData.objects.create(turbidity=value)

        print("Saved to database!")

    except Exception as e:
        print("Error:", e)


#OLD CODE
#def on_message(client, userdata, msg):
 #   try:
 #       payload = msg.payload.decode()
 #       print("Received:", payload)

 #       temperature = float(payload)

        # Save only the value, since 'topic' field no longer exists
  #      SensorData.objects.create(
  #          value=temperature
        
  #      )

  #      print("Saved to database!")

  #  except Exception as e:
   #     print("Error:", e)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()