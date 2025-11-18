# TODO:
# Actually test code to see if it works (it probably doesn't)

import network
import time
import dht
import ujson
from machine import Pin
from umqtt.simple import MQTTClient

# Open config.json file
with open(config.json) as f:
  config = ujson.load(f)
 
# TODO: 
# Set WiFi connection up here (need to figure out how to make it work on enterprise network)

# Sample MQTT credentials
MQTT_CLIENT_ID = config['MQTT_CLIENT_ID']
MQTT_BROKER = config['MQTT_BROKER']
MQTT_USERNAME = config['MQTT_USERNAME']
MQTT_PASSWORD = config['MQTT_PASSWORD']
MQTT_TOPIC = config['MQTT_TOPIC']

MEASUREMENT_DELAY = config['MEASUREMENT_DELAY'] # measure the levels every X seconds.

# Configure DHT11 sensor to pin 16
sensor = dht.DHT11(Pin(16))

# Attempt WiFi connection
max_wait = 15
while max_wait > 0:
  if wlan.isconnected():
    break
  time.sleep(1)
  max_wait -= 1

if wlan.isconnected():
  print("Successfully connected to ", wlan.ipconfig()[0])
else:
  print("ERROR: Could not connect")

# Attempt MQTT Connection
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect()
print("Successfully connected to", MQTT_BROKER)

# Report air temp and humidity to MQTT server
prev_message = ""
while 1:
  print("Measuring temp + humidity...", end="")
  sensor.measure
  message = ujson.dumps({
    "Temperature (F)": (sensor.temperature() * 1.8) + 32,
    "Humidity": sensor.humidity()
  })
  if message != prev_message:
    print("Updating temp + humidity")
    client.publish(MQTT_TOPIC, message)
    prev_message = message
  else:
    print("Temp + humidity unchanged")
  sleep(MEASUREMENT_DELAY)










