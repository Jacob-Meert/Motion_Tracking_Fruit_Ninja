import pygame
import cv2
import numpy
import random
import time
from MotionDetection.BodyCapture import get_frame
import threading 

def launchGame():
    #initialize game and window
    pygame.init()
    window_width = 640
    window_height = 480
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Motion-Box")

    background_color = (0,0,255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            screen.fill(background_color) 

        pygame.display.flip()

    pygame.quit()

launchGame()