import imp
import serial
import time
from flask import Flask, render_template, request
from threading import Thread
from datetime import datetime

from mailService import sendEmail
from thingspeak import sendData


PORT = "COM1"
BAUD_RATE = 9600


obj = { }

obj["TEMPERATURE_SENSOR"] = {"value": 23}
obj["BRIGHTNESS_SENSOR"] = {"value": 64}
obj["DC_MOTOR"] = {"value": 78}
obj["DOOR_COUNTER"] = {"value": 5}
obj["RELAY_COUNTER"] = {"value": 7}


running = True
serialConnection = serial.Serial(PORT, BAUD_RATE)


def receive(serialConnection):
    global running
    while running:
        
        if serialConnection.in_waiting > 0:
            receivedMessage = serialConnection.read_until(b';').decode('ascii')
            processMessage(receivedMessage)
            #serialConnection.reset_input_buffer()
        time.sleep(0.1)


def processMessage(message):
    # Format : "ARDUINO_ID:PIN|VREDNOST;"

    global obj

    objList = message.split(";")
    objList.pop()


    for o in objList:
        m = o.split(":")
        arudinoId = int(m[0])
        pin = str(m[1].split("|")[0])
        val = float(m[1].split("|")[1])
        obj[pin]['value'] = val;

    sendData(
         temperature=obj["TEMPERATURE_SENSOR"]["value"],
         brightness=obj["BRIGHTNESS_SENSOR"]["value"],
         doorCounter=obj["DOOR_COUNTER"]["value"],
         relayCounter=obj["RELAY_COUNTER"]["value"]
    )


#processMessage("0:TEMPERATURE_SENSOR|22;0:BRIGHTNESS_SENSOR|68;0:DOOR_COUNTER|5;0:RELAY_COUNTER|7;")



threadReceiver = Thread(target=receive, args=(serialConnection,))
threadReceiver.start()

threadReceiver = Thread(target=sendEmail)
threadReceiver.start()



app = Flask(__name__)

@app.route('/')
def dashboard():
    global obj
    return render_template("dashboard.html", data=obj)

@app.route('/on/1', methods=['GET'])
def turnOnRelay():
    global serialConnection
    text = getWriteMessageNoVal(0, "RELAY")
    serialConnection.write(text.encode('ascii'))
    print(text)
    return render_template("dashboard.html")

@app.route('/off/1', methods=['GET'])
def turnOffRelay():
    global serialConnection
    text = getWriteMessageNoVal(0, "RELAY")
    serialConnection.write(text.encode('ascii'))
    print(text)
    return render_template("dashboard.html")

@app.route('/on/2', methods=['GET'])
def turnOnServo():
    global serialConnection
    text = getWriteMessageNoVal(0, "SERVO_MOTOR")
    serialConnection.write(text.encode('ascii'))
    print(text)
    return render_template("dashboard.html")

@app.route('/off/2', methods=['GET'])
def turnOffServo():
    global serialConnection
    text = getWriteMessageNoVal(0, "SERVO_MOTOR")
    serialConnection.write(text.encode('ascii'))
    print(text)
    return render_template("dashboard.html")


@app.route('/setPin/3/<value>', methods=['GET'])
def setDigital(value):
    global serialConnection
    
    text = getWriteMessage(0, "DC_MOTOR", int(value))
    serialConnection.write(text.encode('ascii'))
    print(text)
    return render_template("dashboard.html")



def getWriteMessage(controllerId, pin, value):
    return str(controllerId) + ":W:" + str(pin) + ":" + str(value) + ";"

def getWriteMessageNoVal(controllerId, pin):
    return str(controllerId) + ":W:" + str(pin) + ";"

def getReadMessage(controllerId):
    return str(controllerId) + ":R;"


if __name__ == "__main__":
    app.run(port=5000, debug=True)