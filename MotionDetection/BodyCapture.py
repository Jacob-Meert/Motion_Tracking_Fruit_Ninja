import cv2
import mediapipe as mp 
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def get_frame():
    """
    Captures a single frame from the camera.

    Returns:
        np.ndarray: The current frame in RGB format, or None if the camera is not accessible.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return None

    # Capture a single frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Failed to capture frame.")
        return None

    # Convert the frame to RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame
 
