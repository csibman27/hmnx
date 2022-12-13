import random
import time
import json
from paho.mqtt import client as mqtt_client
import nmap

broker = 'broker.emqx.io'
port = 1883
topic = "mqtt/csibman27"
client_id = f'mqtt-csibman27-{random.randint(0, 1000)}'
username = 'csibman27'
password = 'test'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(15)
        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.0.0/24', arguments='-sP')
        output = []
        with open('output.txt', 'a') as outfile:
          for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses']:
              item = nm[h]['addresses']
              if nm[h]['vendor'].values():
                item['vendor'] = list(nm[h]['vendor'].values())[0]
              output.append(item)
          json.dump(output, outfile)
          x = len(output)
          json_data=json.dumps(output)
          client.publish(topic, json_data)
          f = open("outnum", "w")
          f.write(str(x))
          f.close()

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
