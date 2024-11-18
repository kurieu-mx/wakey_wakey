import cv2
import dlib
import pyttsx3
from scipy.spatial import distance
import time
import serial

# Initialize the pyttsx3 for audio alert
engine = pyttsx3.init()

# Initialize the serial connection with Arduino (adjust the port as needed)
arduino_port = 'COM4'  # Change this to the correct port for your Arduino
baud_rate = 9600  # Ensure this matches the baud rate in your Arduino sketch
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Camera setup
cap = cv2.VideoCapture(1)

# Face detection and landmark model
face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(
    r"C:\Users\Eugen\Desktop\Eye_detection\shape_predictor_68_face_landmarks.dat")

# Function to calculate the eye aspect ratio
def Detect_Eye(eye):
    poi_A = distance.euclidean(eye[1], eye[5])
    poi_B = distance.euclidean(eye[2], eye[4])
    poi_C = distance.euclidean(eye[0], eye[3])
    aspect_ratio_Eye = (poi_A + poi_B) / (2 * poi_C)
    return aspect_ratio_Eye

# Timer variables
no_eye_start_time = None
warning_triggered = False
face_detected = False
drowsiness_detected = False

# Main loop
while True:
    _, frame = cap.read()
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector(gray_scale)

    if len(faces) > 0:
        if not face_detected:  # Send signal only once when face is first detected
            arduino.write(b'1\n')  # Send '1' to Arduino when face is detected
            print("Face detected, sent '1' to Arduino for sleep detection mode")
            face_detected = True  # Set flag so it only sends once
        
        for face in faces:
            face_landmarks = dlib_facelandmark(gray_scale, face)
            leftEye = [] 
            rightEye = [] 

            # Left eye points
            for n in range(42, 48):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                rightEye.append((x, y))

            # Right eye points
            for n in range(36, 42):
                x = face_landmarks.part(n).x
                y = face_landmarks.part(n).y
                leftEye.append((x, y))

            # Calculate eye aspect ratio for both eyes
            if leftEye and rightEye:  # Proceed to calculate only if eyes are detected
                right_Eye = Detect_Eye(rightEye)
                left_Eye = Detect_Eye(leftEye)
                Eye_Rat = (left_Eye + right_Eye) / 2
                Eye_Rat = round(Eye_Rat, 2)

                # Drowsiness detection threshold
                if Eye_Rat < 0.25:
                    if no_eye_start_time is None:
                        no_eye_start_time = time.time()  # Start the timer
                    warning_triggered = False  # Reset the warning trigger
                else:
                    no_eye_start_time = None  # Reset timer if eyes are detected
                    if drowsiness_detected:  # Send signal once when drowsiness is over
                        arduino.write(b'0\n')
                        print("Eyes opened, sent '0' to Arduino")
                        drowsiness_detected = False  # Reset the drowsiness flag

            # If eyes are closed for more than 3 seconds
            if no_eye_start_time is not None and (time.time() - no_eye_start_time) > 3:
                if not warning_triggered:
                    # Display alert on the frame
                    cv2.putText(frame, "DROWSINESS DETECTED", (50, 100),
                                cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 210), 3)
                    cv2.putText(frame, "Alert!!!! WAKE UP DUDE", (50, 450),
                                cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 212), 3)

                    # Trigger audio alert
                    engine.say("Alert!!!! WAKE UP DUDE")
                    engine.runAndWait()

                    # Send signal to Arduino to change machine state to 2 (Accelerometer detection)
                    if arduino.is_open:
                        arduino.write(b'2\n')  # Send '2' to Arduino
                        print("Sent '2' to Arduino to change machine state to accelerometer")

                    warning_triggered = True
                    drowsiness_detected = True  # Set drowsiness flag
    else:
        # No face detected
        if face_detected:
            arduino.write(b'0\n')  # Send '0' to Arduino to reset machine state
            print("No face detected, sent '0' to Arduino to return to idle state")
            face_detected = False  # Reset the flag for next face detection

    cv2.imshow("Drowsiness DETECTOR IN OPENCV2", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):  # Press 'q' to stop the program
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()  # Close the serial connection
