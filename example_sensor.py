# Standard
import os
import sys
import time
import json
import logging

from random import seed, randint

# Third party
import paho.mqtt.client
from dotenv import load_dotenv

# Init random
seed(time.time())


# Helper function to get env variable
def get_env(key):
    temp = os.getenv(key)
    if not temp:
        logging.critical("could not find {} from example.env file".format(key))
        sys.exit(1)
    return temp


# Logging settings
logging.basicConfig(level=logging.INFO)

# Start of program
# Load environment variables
logging.info("Starting program")
load_dotenv(sys.argv[1])

mqtt_host = get_env("MQTT_HOST")
mqtt_port = int(get_env("MQTT_PORT"))
mqtt_username = get_env("MQTT_USERNAME")
mqtt_password = get_env("MQTT_PASSWORD")

token = get_env("TOKEN")

# Create MQTT client
client = paho.mqtt.client.Client()
client.username_pw_set(mqtt_username, mqtt_password)

# Connect to broker with client
client.connect(mqtt_host, mqtt_port)
logging.info("Connected to ags broker")

# Create JSON body
current = str(int(time.time()))

data = {
    "token": token,
    "data": {
        "timestamp": current,
        "temperature": randint(20, 30),
        "humidity": randint(30, 40),
        "light": randint(300, 400),
        "soil_moisture": randint(300, 400),
        "water_level": 511
    },
}

body = json.dumps(data)
logging.info(body)

# Publish data to broker
info = client.publish("mqtt/influx", body, 1, False)
info2 = client.publish("mqtt/rethink", body, 1, False)
