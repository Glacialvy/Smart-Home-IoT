import time
import urllib.request
import requests

WRITE_KEY = "BEAYX6F8DLHKJ1A7"
READ_KEY = "OMG426G6MQS5BCGX"
CHANNEL_ID = 1727538

def sendData(temperature, brightness, doorCounter, relayCounter):

    urllib.request.urlopen('https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}'.format(WRITE_KEY, temperature, brightness, doorCounter, relayCounter))
    print("Sent to teamSpeak..")


def getData():
    res = requests.get("https://api.thingspeak.com/channels/{}/feeds.json?api_key={}".format(CHANNEL_ID, READ_KEY))
    # res = requests.get(" https://api.thingspeak.com/channels/{}/fields/{}.json?api_key={}".format(CHANNEL_ID, 2, READ_KEY))

    return res.json()['feeds']