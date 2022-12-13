import random
import json
import sqlite3
from paho.mqtt import client as mqtt_client
import pushDataToDB


broker = 'broker.emqx.io'
port = 1883
topic = 'mqtt/csibman27'
# generate client ID with pub prefix randomly
client_id = f'mqtt-csibman27-{random.randint(0, 100)}'
username = 'csibman27'
password = 'test'

#database_file = 'mqtt.db'


def connect_mqtt() -> mqtt_client:
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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        pushDataToDB.sensorDataHandler(msg.topic, msg.payload)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
