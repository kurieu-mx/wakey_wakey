# Drowsiness Detection and Servo Control System 🚨🤖

This project combines computer vision, embedded systems, and audio feedback to detect drowsiness and manage a servo-controlled machine. It includes real-time monitoring of a user's eye aspect ratio to identify drowsiness, Arduino-controlled hardware states, and optional accelerometer-based control.

## Credits: 

Base drowsiness detection created and owned by https://www.geeksforgeeks.org/python-opencv-drowsiness-detection/

## Features

### Drowsiness Detection System
- **Eye Aspect Ratio Monitoring**: Utilizes OpenCV and Dlib to detect and analyze eye landmarks.
- **Audio Alerts**: Alerts the user with pyttsx3 voice messages when drowsiness is detected.
- **Real-Time Feedback**: Sends signals to an Arduino to change hardware states based on drowsiness detection.

### Servo and Hardware Control (Arduino)
- **State-Based Machine**:
  - *State 0*: Back-and-forth servo motion.
  - *State 1*: Static servo position.
  - *State 2*: Simulated accelerometer control for servo adjustment.
- **Accelerometer Integration**: Reads data from an accelerometer (optional) to control servo behavior dynamically.

## Technologies Used
- **Python**: OpenCV, Dlib, pyttsx3, and serial communication.
- **Arduino**: Servo library for precise motion control and interaction with sensors.

## Getting Started
1. Clone this repository.
2. Install Python dependencies: `pip install opencv-python dlib pyttsx3 pyserial`.
3. Upload the Arduino sketch to your microcontroller.
4. Adjust the Python script's settings (e.g., serial port and camera index) as needed.
5. Run the Python script to start detecting drowsiness and controlling the hardware.

## Applications
- **Driver Monitoring Systems**: Prevent accidents by alerting drivers when drowsiness is detected.
- **Robotics and Automation**: Combine vision-based detection with hardware actions.
- **Research Projects**: Useful for projects involving computer vision and embedded systems integration.
