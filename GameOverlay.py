import pygame
import cv2
import numpy
import random
import time
import threading 

def launchGame():
    #initialize game and window
    pygame.init()
    window_width = 640
    window_height = 480
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Motion-Box")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return
    

    running = True

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
        if not ret:
            print("Error: Unable to read from the camera")
            break

        #Converts frame from BGR to RGB because pygame uses RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = numpy.transpose(frame, (1, 0, 2))
        frame = cv2.flip(frame, 0)  # Flip horizontally
        #Convert the frame to a pygame surface
        frame_surface = pygame.surfarray.make_surface(frame)

        frame_surface = pygame.transform.scale(frame_surface,(window_width,window_height))
        
        screen.blit(frame_surface,(0,0))

        # Update the display
        pygame.display.flip()
    cap.release()
    pygame.quit()

launchGame()