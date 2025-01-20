import pygame
import cv2
import numpy as np
import random
import time
import threading 
import FruitNinja
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def launchGame():
    sprites = pygame.sprite.Group()
    lastSpawn = 0
    currentTime = 0

    #initialize game and window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Motion-Box")

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return
    

    Clock = pygame.time.Clock()

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

            currentTime = pygame.time.get_ticks()

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

            try:
                landmarks = results.pose_landmarks.landmark
                print(getRightHandCoordinates(landmarks))
            except AttributeError as e:
                print(f"Landmark extraction failed: {e}")

            mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS)

            #Converts image from BGR to RGB because pygame uses RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
             
            image = cv2.flip(np.transpose(image, (1, 0, 2)), 0)  # Flip horizontally
            #Convert the frame to a pygame surface
            
            frame_surface = pygame.surfarray.make_surface(image)

            frame_surface = pygame.transform.scale(frame_surface,(screen.get_width(),screen.get_height()))
            
            screen.blit(frame_surface,(0,0))

            if currentTime - lastSpawn > 3000:
                sprites.add(FruitNinja.fruit(screen.get_width(), screen.get_height()))
                lastSpawn = currentTime

            #update sprites at each tick
            sprites.update()
            sprites.draw(screen)

                # Update the display
            pygame.display.flip()

            #cap frame rate
            Clock.tick(100)

        cap.release()
        pygame.quit()

def getRightHandCoordinates(landmarks):
    finger = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value]
    return(finger.x,finger.y)

def getLeftHandCoordinates(landmarks):
    finger = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value]
    return(finger.x,finger.y)

def getRightFootCoordinates(landmarks):
    foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
    return(foot.x,foot.y)

def getLeftFootCoordinates(landmarks):
    foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
    return(foot.x,foot.y)









launchGame()