#include <Servo.h>

Servo xServo;
Servo waterServo;
int direction = 1;
int rotation = 1000;

// Declare pins for the accelerometer
int xPin = A0;
int yPin = A1;
int zPin = A2;

void setup() {
  Serial.begin(9600);
  xServo.attach(8);
  waterServo.attach(9);
  pinMode(13, OUTPUT);
}

void loop (){
  if (Serial.available > 0){
    char input = Serial.read();
    if (input == 'd'){
      rotation = rotation + 40;
    }
    else if (input == 'a'){
      rotation = rotation - 40;
    }
    else if (input == 's'){
      waterServo.writeMicroseconds (1540);
      delay (1500);
    }
  }
 
}

