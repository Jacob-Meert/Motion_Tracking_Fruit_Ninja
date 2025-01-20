import pygame
import random
import numpy as np

class limbTracker(pygame.sprite.Sprite):
    def __init__(self, width, length):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.windowWidth = width
        self.windowLength = length

    def update(self, point):
        self.rect.x = int((1-point[0])*self.windowWidth)
        self.rect.y = int(point[1]*self.windowLength)

    def draw(self,screen):
        screen.blit(self.image,self.rect)

class fruit(pygame.sprite.Sprite):
    images = ["Orange.png","Strawberry.png","Lemon.png","Grapes.png","Apple.png", "Banana.png", "Watermelon.png", "Pineapple.png"]
    sizing = [(190,190), (152,160), (152,160), (205,205), (190,190), (190,190), (220, 190), (222, 257)]

    def __init__(self, windowWidth, windowHeight):
        super().__init__()
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth

        index = random.randint(0,7)
        self.image = pygame.image.load("Fruit_images/" + self.images[index]).convert_alpha()  # Load image with transparency
        self.image = pygame.transform.scale(self.image, (self.sizing[index][0]*4/10,self.sizing[index][1]*4/10))
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = windowHeight+50
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 40) + random.randint(-15,15))*(np.pi/180)

        self.xMotion = np.cos(self.angle)*random.randint(40,45)
        self.yMotion = np.sin(self.angle)*random.randint(-55,-50)
        

    def update(self, points):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion += 1.5

        if self.rect.y > self.windowHeight+60:
            self.kill()

        if self.checkCollisions(points):
            self.kill()

    def checkCollisions(self, points):
        for point in points:
            if self.rect.collidepoint((int((1-point[0])*self.windowWidth),int(point[1]*self.windowHeight))):
                return True
        return False