from paho.mqtt import client as _mqtt
import json

class MQTT():
    def __init__(self, broker:str, port:int, numero_serie:str, subscriptions:list = [], username:str = None, password:str = None, qos:int = 0):
        self._broker = broker
        self._port = port
        self._subscriptions = subscriptions
        self._qos = qos
        self._numero_serie = numero_serie
        self._username = username
        self._password = password
        self.__setup_client()
        self.__start()
    
    def __setup_client(self,):
        self._client = _mqtt.Client(client_id=self._numero_serie)
        self._client.username_pw_set(username=self._username, password=self._password)
        self._client.on_connect = self.__on_connect
        self._client.on_message = self.__on_message
        self._client.on_publish = self.__on_publish

    def __start(self,):
        self._client.connect(host=self._broker, port=self._port,)
        self.__subscrition(self._subscriptions)
        self._client.loop_start()
    
    def stop(self,):
        self._client.loop_stop()
        self._client.disconnect()

    def __on_connect(self, client: _mqtt.Client, userdata, flags, rc):
        print('MQTT connected!')
        # self.subscrition()
    
    def __on_message(self, client: _mqtt.Client, userdata, msg: _mqtt.MQTTMessage):
        print("Topic msg mqtt: "+ msg.topic)
        print("\tMSG: "+ msg.payload)
    
    def __on_publish(self, client: _mqtt.Client, userdata, mid):
        print('on_publish: '+str(mid))
        
        
    def publish(self, topic:str, payload:dict, qos:int=1 ):
        if self._numero_serie not in topic:
            if topic.startswith("/"): topic = topic.removeprefix("/")
            topic = self._numero_serie+"/"+topic
            
        self._client.publish(topic=topic, payload=json.dumps(payload), qos=qos)
    
    def publish_data(self, topic:str, payload:dict, qos:int=1 ):
        self.publish("/data/"+topic, payload, qos)

    def publish_status(self, topic:str, payload:dict, qos:int=1 ):
        self.publish("/status/"+topic, payload, qos)

    def __subscrition(self, _list:list):
        for topic in _list:
            print("Subscribed to topic: "+topic)
            self._client.subscribe(topic=topic)
    
    def on_loop_sender(self,):
        while(1):
            try:
                if self._queue.qsize():
                    ret = self.publish(topic='wagner/teste', payload=self._queue.get())
                    print(ret)
            except Exception as err:
                print(f"ERROR: {err}")
                ...