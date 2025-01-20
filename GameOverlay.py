import pygame
import cv2
import numpy as np
import random
import time
import threading 
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def launchGame():
    #initialize game and window
    pygame.init()
    window_width = 640
    window_height = 480
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Motion-Box")

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return
    

    running = True
    with mp_pose.Pose(min_detection_confidence = 0.6, min_tracking_confidence = 0.6) as pose:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
                # Check for KEYDOWN event inside the event loop
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Space Pressed!")
                        running = False  

            #capture frame
            ret, frame = cap.read()
            print(f"Camera Frame Retrieved: {ret}")
            if not ret:
                print("Error: Unable to read from the camera")
                break

            #Converts image from BGR to RGB because pygame uses RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
             #Makes detection
            results = pose.process(image)

            #Convert image back to BGR

            image.flags.writeable = True
            image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS)

            #Converts image from BGR to RGB because pygame uses RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             
            image = cv2.flip(np.transpose(image, (1, 0, 2)), 0)  # Flip horizontally
            #Convert the frame to a pygame surface
            
            frame_surface = pygame.surfarray.make_surface(image)

            frame_surface = pygame.transform.scale(frame_surface,(window_width,window_height))
            
            screen.blit(frame_surface,(0,0))

            # Update the display
            pygame.display.flip()
        cap.release()
        pygame.quit()

launchGame()