import paho.mqtt.client as mqtt


def on_connect(client , userdata, flags, rc):
    print("mqtt conectado ")

    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" Teste_detect"+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.ness.com.br", 1883)

client.loop_forever()