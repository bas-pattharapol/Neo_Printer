
import random
import time
import json
from paho.mqtt import client as mqtt_client


broker = '10.11.1.1'
port = 1883
topic = "/line/1/send"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'plc1'
password = 'plc@2021'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = {"version":0.1,"Code":3,"index":10,"barcode":5555555,"code_type":"itf"}
    while True:
        time.sleep(3)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        d = json.loads(msg.payload)
        print("code : " + str(d["Code"]))

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

    #subscribe(client)
    #client.loop_forever()


if __name__ == '__main__':
    run()