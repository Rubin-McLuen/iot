import time
import paho.mqtt.client as paho
from gpiozero import LED

broker = "172.16.208.188"
broker = "test.mosquitto.org"
led = LED(17)

def onMessage(client, userdata, message):
	time.sleep(1)
	msg = str(message.payload.decode("utf-8"))

	print("Received: ", msg)
	global led
	if msg == "State=on":
		led.on()
	elif msg == "State=off":
		led.off()


def onConnect( client, userdata, flags, rc):
	print("Connecting")
	if rc == 0:
		print("Connect Ok")
	else:
		print("Bad Connection")



# def onPublish(client, userdata, result)

def mqttConnection():
	client = paho.Client("Rubin")
	client.on_message = onMessage
	client.on_connect = onConnect

	print("connecting to broker", broker)
	client.connect(broker)  # connect
	client.loop_start()
	client.subscribe("sbhtest")
	client.publish("sbhtest", "")  # publish
	while (True):
		time.sleep(4)

	client.loop_stop()

	return client


mqttConnection()