import time
import paho.mqtt.client as paho

broker = "172.16.208.188"
broker = "test.mosquitto.org"

def publish(message):
	client = paho.Client("http")
	# client.on_message = onMessage

	client.connect(broker)  # connect
	client.loop_start()
	client.subscribe("sbhtest")
	client.publish("sbhtest", message)
	client.loop_stop()