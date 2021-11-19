import time
import json
from mqtt import mqtt_publisher
import configparser
import os
import threading
from gpioService import Relay

PROJECT_CONF = os.path.dirname(os.path.abspath(__file__)) + '/settings.ini'

class mqttController:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(PROJECT_CONF)
        self.rl = Relay()
        self.mqtt_client = mqtt_publisher(
            server=config['MQTT']['host'],
            port=int(config['MQTT']['port']),
            client_id=config['MQTT']['client_id'],
            user_name=config['MQTT']['user_name'],
            password=config['MQTT']['password'])

        self._sm = threading.Thread(target=self.__subscribe_message)
        self._sm.start()

        self._shadow = threading.Thread(target=self.__shadow)
        self._shadow.start()

        self.mqtt_client.client.subscribe('Lock/status')

    def __subscribe_message(self):
        while True:
            try:
                time.sleep(.05)
                if self.mqtt_client.msg is not None:
                    self.process_lock_state()
            except:
                pass

    def __shadow(self):
        while True:
            time.sleep(.5)
            try:
                self.publish('shadow/status', "{"+"\"code\":{}, \"message\":\"{}\"".format('200', self.rl.status)+"}")
            except:
                pass

    def process_lock_state(self):
        msg = self.mqtt_client.get_msg()
        try:
            msg = json.loads(msg.payload)
            if msg['is_opened'] is True:
                self.rl.lock(msg['lock'])
            self.say_('200', 'Ok')
        except Exception as e:
            self.say_('500', e)
            return False

    def say_(self, code, message):
        self.publish('Lock/response',"{"+"\"code\":{}, \"message\":\"{}\"".format(code, message)+"}")

    def publish(self, topic, message):
        self.mqtt_client.client.publish(topic=topic, payload=message)
        pass
