import pygame
import random
import numpy as np

class fruit(pygame.sprite.Sprite):
    def __init__(self, windowWidth):
        super().__init__()
        self.image = pygame.Surface((50, 50))  
        self.image.fill((255, 0, 0))  

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = 0
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 40) + random.randint(-15,15))*(np.pi/180)

        self.xMotion = np.cos(self.angle)*6
        self.yMotion = np.sin(self.angle)*8
        

    def update(self):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion -= 0.1