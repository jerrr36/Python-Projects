import paho.mqtt.client as mqtt
import time


#on connection function
def on_connect(client, userdata, flags, rc):
    print(f'Connected to hivemq broker with result code {str(rc)}')

    client.subscribe("esp/test")
    time.sleep(1)


#function to parse messages
def on_message(client, userdata, msg):
    print(f'Topic: {msg.topic}  Payload: {msg.payload}')


client = mqtt.Client()
time.sleep(1)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com")
time.sleep(2)

client.loop_forever(timeout=20, max_packets=20)
