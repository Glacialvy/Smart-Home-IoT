#include <Servo.h>

#define DC_MOTOR 3
#define RELAY 4
#define SERVO_MOTOR 9
#define ULTRASONIC_ECHO 10
#define ULTRASONIC_TRIGGER 11

#define POTENCIOMETER A0
#define TEMPERATURE_SENSOR A1
#define BRIGHTNESS_SENSOR A2

#define ARDUINO_ID 0

int state = LOW;

int potAnalogValue = 0;
int tempAnalogValue = 0;
int briAnalogValue = 0;
int potTemp = 0;

int servoCounter = 0;
int relayCounter = 0;

double temperature;
int pot;
int brightness;

bool doorOpened = false;

unsigned long previousMillis = 0;
const long interval = 1000;
int timer = 60;

Servo servo;


void setup() {
  Serial.begin(9600);
  
  pinMode(DC_MOTOR, OUTPUT);
  pinMode(RELAY, OUTPUT);
  pinMode(SERVO_MOTOR, INPUT);
  pinMode(ULTRASONIC_ECHO, INPUT);
  pinMode(ULTRASONIC_TRIGGER, OUTPUT);
 
  digitalWrite(RELAY, LOW);
  servo.attach(SERVO_MOTOR);
  
 // Serial.println("Write a command in format: ARDUINO_ID:W/R:PIN:VREDNOST;");
}


void led_state() {
	state = !state;
  	digitalWrite(RELAY, state);
}


void dc_motor_speed() {
  potAnalogValue = analogRead(POTENCIOMETER);
  pot = map(potAnalogValue, 0, 1023, 0, 255);
  // Serial.println((String)"DC Motor Speed: " + pot);
  
  if (potTemp != pot) {
    analogWrite(DC_MOTOR, pot);
    potTemp = pot;
  }
}


void distance_measure() { 
  digitalWrite(ULTRASONIC_TRIGGER, LOW);
  delayMicroseconds(2);
  digitalWrite(ULTRASONIC_TRIGGER, HIGH);
  delayMicroseconds(10);
  digitalWrite(ULTRASONIC_TRIGGER, LOW);
  
  double readEcho = pulseIn(ULTRASONIC_ECHO, HIGH);
  double distance = readEcho * 0.0343 * 0.5;
  // Serial.println((String)"Distance: " + distance);
  
  if (distance <= 5) {
  	servo.write(90);
    doorOpened = true;
  }
  
  if (doorOpened && distance >= 5) {
      servo.write(0);
      servoCounter++;
      doorOpened = false;
  }
  
  /*
  if (distance <= 5) {
  	servo.write(90);
  }
  else {
  	servo.write(0);
  }
  */
}


double temperature_measure(){
	tempAnalogValue = analogRead(TEMPERATURE_SENSOR);
  	temperature = (double)tempAnalogValue * 500 / 1024 - 50;
  	// Serial.println((String)"Temperature: " + temperature);
  	return temperature;
}


int brightness_measure(){  
	briAnalogValue = analogRead(BRIGHTNESS_SENSOR);
  	brightness = map(briAnalogValue, 1, 310, 0, 100);
  	// Serial.println((String)"Brightness: " + brightness);
  	return brightness;
}


void countdown(){
  unsigned long currentMillis = millis();
  
	if (currentMillis - previousMillis >= interval) {
  	    previousMillis = currentMillis;
    	timer--;
    	// Serial.println((String) "Timer: " + timer);

      	if (timer <= 0) {
      	  timer = 60;
        Serial.println(
          (String) ARDUINO_ID + ":" + "TEMPERATURE_SENSOR" + "|" + temperature + ";" +
          (String) ARDUINO_ID + ":" + "BRIGHTNESS_SENSOR" + "|" + brightness + ";" + 
          (String) ARDUINO_ID + ":" + "DOOR_COUNTER" + "|" + servoCounter + ";" + 
          (String) ARDUINO_ID + ":" + "RELAY_COUNTER" + "|" + relayCounter + ";"
           );
    	}
  	}
}


void loop() {
  
  countdown();
  
  if (Serial.available() > 0){
    
  	String input = Serial.readStringUntil(';');
    int i = input.indexOf(':');
    
    if (i > 0) {
    	String arduinoId = input.substring(0, i);
        int id = arduinoId.toInt();
      	char w_r = input.charAt(i+1);
      
      if (w_r == 'W') {
      	int s = i + 3;
        i = input.indexOf(':', s);
        String pin = input.substring(s, i);
        String val = input.substring(i+1);
        int p = pin.toInt();
        int v = val.toInt();
        
        if (id != ARDUINO_ID) {
          //SEND
        }
        else {
          if (pin == "RELAY") {
          	led_state();
            relayCounter++;
           // Serial.println((String) "Relay Counter: " + relayCounter);
           // Serial.println("led state changed successfully!");
          }
          
          else if (pin == "DC_MOTOR") {
            int dcSpeed = map(v, 0, 100, 0, 255);
          	analogWrite(DC_MOTOR, dcSpeed);
           // Serial.println((String)"DC motor speed changed successfully to: " + dcSpeed);
          }
          
          else if (pin == "SERVO_MOTOR") {
            
            if (doorOpened) {
             // Serial.println("Door is already open..");
            }
            
            else {
              servo.write(90);
              servoCounter++;
             // Serial.println("Door opened!");
             // Serial.println((String) "Servo Counter: " + servoCounter);
            }
          }
        }
      }
    }
  }
  
  else {
  	dc_motor_speed();
    distance_measure();
    temperature_measure();
    brightness_measure();
  }
}