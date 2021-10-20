
from detect_button import Detect
from Mqtt import MQTT
from threading import Thread


if __name__ == "__main__":

   
    mqtt = MQTT(
        broker="mqtt.ionic.health",
        port=1884,
        numero_serie="test_wagner",
        subscriptions=["detector_python"],
        username="ness",
        password="ness123"
        )
    _detect = Detect(mqttClient=mqtt)
