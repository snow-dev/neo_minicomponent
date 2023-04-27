import sys
import time
import lirc
import os
from dotenv import load_dotenv

from Adafruit_IO import MQTTClient

load_dotenv()

ADAFRUIT_IO_KEY = os.getenv("ADAFRUIT_IO_KEY")
ADAFRUIT_IO_USERNAME = os.getenv("ADAFRUIT_IO_USERNAME")
FEED_ID = os.getenv("FEED_ID")

ir_client = lirc.Client()

def connected(client):
    print('Connected to Adafruit IO!  Listening for {0} changes...\n'.format(FEED_ID))
    client.subscribe(FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print('Subscribed to {0} with QoS {1}'.format(FEED_ID, granted_qos[0]))

def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload == "On":
        # print("Stereo On")
        ir_client.send_once("Pioneer_CU-XR032", "KEY_POWER")
        time.sleep(5)
        ir_client.send_once("Pioneer_CU-XR032", "AUX")
        time.sleep(5)
        ir_client.send_start("Pioneer_CU-XR032", "KEY_VOLUMEUP")
        time.sleep(5)
        ir_client.send_stop("Pioneer_CU-XR032", "KEY_VOLUMEUP")
    elif payload == "Off":
        # print("Stereo Off")
        ir_client.send_once("Pioneer_CU-XR032", "KEY_POWER")

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.on_subscribe  = subscribe

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.  Note there are other options for running the message loop like doing
# so in a background thread.  See the MQTT client docs for details.

client.loop_blocking()
