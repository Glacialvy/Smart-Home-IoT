import time
import urllib.request
import requests

WRITE_KEY = "WriteKeyhere"
READ_KEY = "ReadKeyHere"
CHANNEL_ID = 123123123

def sendData(temperature, brightness, doorCounter, relayCounter):

    urllib.request.urlopen('https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}'.format(WRITE_KEY, temperature, brightness, doorCounter, relayCounter))
    print("Sent to teamSpeak..")


def getData():
    res = requests.get("https://api.thingspeak.com/channels/{}/feeds.json?api_key={}".format(CHANNEL_ID, READ_KEY))
    # res = requests.get(" https://api.thingspeak.com/channels/{}/fields/{}.json?api_key={}".format(CHANNEL_ID, 2, READ_KEY))

    return res.json()['feeds']
