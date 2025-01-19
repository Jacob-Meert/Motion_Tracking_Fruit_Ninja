import cv2
import mediapipe as mp 
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def bodyCap():

    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)  # Default camera
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        exit()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Frame capture failed. Exiting.")
            break

        # Display the frame
        cv2.imshow("MotionBox", frame)

        # Exit on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
 
