import pygame
import random
import numpy as np

class fruit:
    def __init__(self, windowWidth):
        super().__init__()
        self.image = pygame.Surface((50, 50))  
        self.image.fill((255, 0, 0))  

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = 0
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 40) + random.randint(-10,10))*(np.pi/180)

        self.xMotion = np.cos(self.angle)
        self.yMotion = np.sin(self.angle)
        

    def update(self):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion -= 0.082

        if self.rect.y < 0:
            return "Dropped Out"