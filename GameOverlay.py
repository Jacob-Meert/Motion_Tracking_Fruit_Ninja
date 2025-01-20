import pygame
import cv2
import numpy
import random
import time
from MotionDetection.BodyCapture import get_frame
import threading 
import FruitNinja

def launchGame():
    sprites = pygame.sprite.Group()
    lastSpawn = 0
    currentTime = 0

    #initialize game and window
    pygame.init()
    window_width = 640
    window_height = 480
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Motion-Box")

    background_color = (0,0,255)

    Clock = pygame.time.Clock()

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

        currentTime = pygame.time.get_ticks()

        # Fill the screen with the background color
        screen.fill(background_color)

        if currentTime - lastSpawn > 3000:
            sprites.add(FruitNinja.fruit(window_width))
            lastSpawn = currentTime

        #update sprites at each tick
        sprites.update()
        sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        #cap frame rate
        Clock.tick(60)

    pygame.quit()


launchGame()