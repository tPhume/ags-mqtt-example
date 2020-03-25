# standard
import os
import sys
import logging

# non-standard
import paho.mqtt.client
from dotenv import load_dotenv


# utility function to help get env
# will exit if error occurs
def get_env(key):
    temp = os.getenv(key)
    if not temp:
        logging.critical("could not find {} from ags.env file".format(key))
        sys.exit(1)
    return temp


# settings
logging.basicConfig(level=logging.INFO)

# start of program
# Load environment variables
logging.info("starting program")
load_dotenv("hive.env")

mqtt_host = get_env("MQTT_HOST")
mqtt_port = int(get_env("MQTT_PORT"))

# Connect to MQTT broker
client = paho.mqtt.client.Client("", True, None)
client.connect(mqtt_host, mqtt_port)
logging.info("connected to hivemq test broker")

# Publish message
info = client.publish("/test", "hello hive", 0)
logging.info("waiting for confirm")
info.wait_for_publish()
logging.info("Confirmed {}".format(info.is_published()))
