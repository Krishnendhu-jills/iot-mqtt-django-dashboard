import paho.mqtt.client as mqtt
import json

from dashboard.models import SensorData
from django.utils import timezone

# Django Channels imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


BROKER = "broker.emqx.io"
PORT = 1883

# ESP32 Topic
QUALITY_TOPIC = "water/quality"


def send_alert(message):

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "alerts",
        {
            "type": "send_alert",
            "message": message
        }
    )




def check_alerts(temperature, ph, turbidity):

    if ph > 8.5:
        return "⚠️ pH too high"

    elif ph < 6.5:
        return "⚠️ pH too low"

    elif temperature > 35:
        return "⚠️ Temperature too high"

    elif turbidity == 0:
        return "⚠️ Water is Turbid"

    return None



def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)

    client.subscribe(QUALITY_TOPIC)



def on_message(client, userdata, msg):

    try:
        payload = msg.payload.decode()
        print("Received:", payload)

        data = json.loads(payload)

        temperature = data["temperature"]
        ph = data["ph"]
        turbidity = data["turbidity"]

         # CHECK ALERT
        alert_message = check_alerts(temperature, ph, turbidity)

        if alert_message:
            print("ALERT:", alert_message)   # shows in terminal

        # Save to database
        SensorData.objects.create(
            temperature=temperature,
            ph=ph,
            turbidity=turbidity,
            timestamp=timezone.now()
        )

        print("Saved to database!")

     

    except Exception as e:
        print("Error:", e)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()