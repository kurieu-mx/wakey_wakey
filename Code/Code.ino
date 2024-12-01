#include <Servo.h>

Servo xServo;
Servo waterServo;
int machinestate = 0;
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

  // Inform the user about the available commands
  Serial.println("Type '0' for state 0 (Back and Forth Servo Motion).");
  Serial.println("Type '1' for state 1 (Static Servo Position).");
  Serial.println("Type '2' for state 2 (Accelerometer Control).");
}

void loop() {
  // Check for input from the Serial Monitor
  if (Serial.available() > 0) {
    char input = Serial.read();
    if (input == '1') {
      machinestate = 1;
      Serial.println("Machine State set to 1: Static Servo.");
    } 
    else if (input == '2') {
      machinestate = 2;
      Serial.println("Machine State set to 2: Accelerometer-Controlled Servo.");
    }
    else if (input == '0') {
      machinestate = 0;
      Serial.println("Machine State set to 0: Back and Forth Servo Motion.");
    }
  }

  // Servo control based on machinestate
  if (machinestate == 0) {
    Serial.println("In Machine State 0: Servo Back and Forth Motion");
    xServo.writeMicroseconds(rotation);
    waterServo.writeMicroseconds(1500);
    
    // Adjust rotation based on the direction
    if (direction == 1) {
      rotation = rotation + 40;
      if (rotation >= 2500) {
        direction = -1;  // Switch to decreasing
        Serial.println("Servo reached max position, changing direction.");
      }
    } else {
      rotation = rotation - 40;
      if (rotation <= 500) {
        direction = 1;  // Switch to increasing
        Serial.println("Servo reached min position, changing direction.");
      }
    }
    
    delay(10);  // Delay after each step
  }

  // Static servo position when machinestate is 1
  if (machinestate == 1) {
    Serial.println("In Machine State 1: Holding Servo Position.");
    xServo.writeMicroseconds(rotation);  // Neutral position, adjust as necessary
  }

  // Accelerometer-based control for machinestate 2
  if (machinestate == 2) {
    Serial.println("In Machine State 2: Simulated Accelerometer Control.");
    
    // Uncomment these lines if you have an accelerometer connected
    int xReading = analogRead(xPin);
    int yReading = analogRead(yPin);
    int zReading = analogRead(zPin);
    
    float xVoltage = (xReading / 1023.0) * 3.3;
    float yVoltage = (yReading / 1023.0) * 3.3;
    float zVoltage = (zReading / 1023.0) * 3.3;
    
    // Convert voltage to acceleration
    float xAcceleration = (xVoltage - 1.14) / 0.3;
    float yAcceleration = (yVoltage - 1.14) / 0.3;
    float zAcceleration = (zVoltage - 1.14) / 0.3;

    // Example condition based on simulated accelerometer input
    if (zAcceleration < 0 && yAcceleration < 0 && xAcceleration < 0) {
      delay(2000);
      waterServo.writeMicroseconds(1500);
      
      if (direction == 1) {
        rotation = 100;
      } else {
        rotation = rotation - 100;
      }
    }
    
    delay(2000);  // Simulated delay for the action
    machinestate = 0;  // Return to idle state after performing action
  }

  delay(100);  // Prevent spamming the Serial output
}
