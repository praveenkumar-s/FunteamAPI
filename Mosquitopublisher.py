import paho.mqtt.client as mqtt
#import GlobalConfig


def Publish(topic, message,  retain=False):
    client = Mqtt.Client()
    client.connect("iot.eclipse.org", 1883, 60)
    client.publish(topic=topic, payload=message )
    client.disconnect()
    client = None


