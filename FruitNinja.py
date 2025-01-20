import pygame
import random
import numpy as np

class fruit(pygame.sprite.Sprite):
    images = ["Orange.png","Strawberry.png","Lemon.png","Cherries.png","Grapes.png","Apple.png", "Banana.png", "Watermelon.png", "Pineapple.png"]
    sizing = [(190,190), (152,160), (152,160), (152,152), (205,205), (190,190), (190,190), (220, 190), (222, 257)]

    def __init__(self, windowWidth, windowHeight, difficulty = 1):
        super().__init__()
        self.windowHeight = windowHeight

        index = random.randint(0,8)
        self.image = pygame.image.load("Fruit_images/" + self.images[index]).convert_alpha()  # Load image with transparency
        self.image = pygame.transform.scale(self.image, (self.sizing[index]))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = windowHeight+50
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 40) + random.randint(-15,15))*(np.pi/180)

        self.xMotion = np.cos(self.angle)*difficulty*random.randint(40,45)
        self.yMotion = np.sin(self.angle)*difficulty*random.randint(-55,-50)
        

    def update(self):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion += 1.5

        if self.rect.y > self.windowHeight+60:
            self.kill()