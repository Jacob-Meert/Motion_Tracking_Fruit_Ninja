import pygame
import random
import numpy as np

class fruit(pygame.sprite.Sprite):
    def __init__(self, windowWidth, windowHeight, difficulty = 1):
        super().__init__()
        self.windowHeight = windowHeight
        self.image = pygame.Surface((50, 50))  
        self.image.fill((255, 0, 0))  

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = windowHeight+50
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 40) + random.randint(-15,15))*(np.pi/180)

        self.xMotion = np.cos(self.angle)*difficulty*random.randint(9,12)
        self.yMotion = np.sin(self.angle)*difficulty*random.randint(-21,-18)
        

    def update(self):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion += 0.4

        if self.rect.y > self.windowHeight+60:
            self.kill()