import paho.mqtt.client as mqtt
import time
import threading

class mqtt_publisher:
    msg = None

    def __init__(self,
                 server: str = '',
                 port: int = 0,
                 client_id: str = '',
                 user_name: str = '',
                 password: str = '',
                 clean_session: bool = True):
        self.server = server
        self.port = port
        self.client_id = client_id
        self.user_name = user_name
        self.password = password
        self.clean_session = clean_session

        self.client = mqtt.Client(
            client_id=client_id,
            clean_session=clean_session,
            transport='tcp')
        self.client.username_pw_set(user_name, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect
        #self.client.ws_set_options()
        #self.client.tls_set()
        self.client.connect(server, port, 60)
        self.client.connected_flag = False
        while not self.client.is_connected():  # wait in loop
            self.client.loop()
            time.sleep(1)
            if self.client.is_connected():
                print('Connected')
                break
            print('not connected')

        self._poll = threading.Thread(target=self._pooling)
        self._poll.start()

    def get_msg(self):
        msg = self.msg
        self.msg = None
        return msg

    def _pooling(self):

        try:
            while True:
                time.sleep(1)
                if not self.client.is_connected():
                    self.connect()
        except:
            pass

    def connect(self):
        self.client.disconnect()
        self.client.connect(self.server, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(userdata, flags,"Connected with result code " + str(rc))

        if rc == 0:
            self.client.connected_flag = True
            print("connected OK")
            return

        print("Failed to connect to %s, error was, rc=%s" % rc)
        # handle error here

    def on_message(self, client, userdata, msg):
        print(msg.topic + " *** " + str(msg.payload))
        self.msg = msg

    def on_publish(self, userdata, result, mid):  # create function for callback
        print("data published \n",userdata, result)
        pass

    def on_disconnect(self, userdata, rc):
        print("client disconnected ok")

