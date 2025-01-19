import pygame
import cv2
import numpy
import random
import time

def launchGame():
    #initialize game and window
    pygame.init()
    window_width = 640
    window_height = 480
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Motion-Box")

    background_color = (0,0,255)

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

        # Fill the screen with the background color
        screen.fill(background_color)

        # Update the display
        pygame.display.flip()
    pygame.quit()

launchGame()