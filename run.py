#!/usr/bin/env python3
from mqttController import mqttController
import time


mqtt_client = mqttController()

while not mqtt_client.mqtt_client.client.is_connected():
    time.sleep(1)
    pass

mqtt_client.mqtt_client.client.loop_start()
