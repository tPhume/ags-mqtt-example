# standard
import os
import sys
import time
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


# function to log message on publish
def on_publish_callback(client, user_data, mid):
    logging.info(mid)


# settings
logging.basicConfig(level=logging.INFO)

# start of program
# Load environment variables
logging.info("starting program")
load_dotenv("ags.env")

mqtt_host = get_env("MQTT_HOST")
mqtt_port = int(get_env("MQTT_PORT"))
mqtt_username = get_env("MQTT_USERNAME")
mqtt_password = get_env("MQTT_PASSWORD")

# Create new MQTT client
client = paho.mqtt.client.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_publish = on_publish_callback

# Establish connection to broker
client.connect(mqtt_host, mqtt_port)
logging.info("connected to ags broker")

# Publish to broker
client.publish("mqtt/hello-world", "hello world - 1", 1)
client.publish("mqtt/hello-world", "hello world - 2", 1)

# Wait for 3 seconds (to allow callback to run) before exiting
client.loop_start()
time.sleep(3)
client.loop_stop()