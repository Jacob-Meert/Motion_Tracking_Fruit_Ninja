import pygame
import random
import numpy as np

class limbTracker(pygame.sprite.Sprite):
    def __init__(self, width, length):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)  # Enable transparency
        self.image.fill((0, 0, 0, 0))  # Black color with 50% transparency (128 out of 255)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.windowWidth = width
        self.windowLength = length
        self.trail = []
        self.trail_length = 20

    def update(self, point):
        self.rect.x = int((1-point[0])*self.windowWidth)
        self.rect.y = int(point[1]*self.windowLength)

        self.trail.append({
                "x": self.rect.x,
                "y": self.rect.y,
                "radius": 20,  # Start as a large circle
                "color": (255, 0, 0),  # Start as red
                "alpha": 255  # Start fully opaque
            })

        # Update the trail to shrink, fade, and change color
        for circle in self.trail:
            circle["radius"] -= 1  # Gradually shrink the circle
            circle["alpha"] -= 5  # Gradually fade out
            # Gradually transition color to white
            circle["color"] = (
                min(255, circle["color"][0] + 10),  # Increase red to 255
                min(255, circle["color"][1] + 10),  # Increase green to 255
                min(255, circle["color"][2] + 10)   # Increase blue to 255
            )

        # Remove circles that have faded out or become too small
        self.trail = [circle for circle in self.trail if circle["alpha"] > 0 and circle["radius"] > 0]

    def draw(self, screen):
    # Draw the trail
        for circle in self.trail:
            surface = pygame.Surface((circle["radius"] * 2, circle["radius"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*circle["color"], circle["alpha"]), (circle["radius"], circle["radius"]), circle["radius"])
            screen.blit(surface, (circle["x"] - circle["radius"], circle["y"] - circle["radius"]))

            screen.blit(self.image, self.rect)


class fruit(pygame.sprite.Sprite):
    images = ["Orange.png","Strawberry.png","Lemon.png","Grapes.png","Apple.png", "Banana.png", "Watermelon.png", "Pineapple.png"]
    sizing =   [(142, 142),
                (114, 120),
                (114, 120),
                (153, 153),
                (142, 142),
                (142, 142),
                (165, 142),
                (166, 192)]

    def __init__(self, windowWidth, windowHeight):
        super().__init__()
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth

        index = random.randint(0,7)
        self.image = pygame.image.load("Fruit_images/" + self.images[index]).convert_alpha()  # Load image with transparency
        self.image = pygame.transform.scale(self.image, self.sizing[index])
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, windowWidth - self.rect.width)
        self.rect.y = windowHeight+50
      
        self.angle = ((((self.rect.x / windowWidth) * 100) + 55) + random.randint(-15,15))*(np.pi/180)

        self.xMotion = np.cos(self.angle)*random.randint(40,45)
        self.yMotion = np.sin(self.angle)*random.randint(-55,-50)

        self.alive = True

        self.missReturn = False
        
        self.ding_sound = pygame.mixer.Sound('Sounds/collision_noise.mp3')

    def update(self, points):
        self.rect.x += self.xMotion
        self.rect.y += self.yMotion

        self.yMotion += 1.5

        if self.rect.y > self.windowHeight+self.rect.height:
            self.kill()
            return self.missReturn 
        
        if self.rect.x > self.windowWidth + self.rect.width:
            self.kill()
            return self.missReturn
        
        if self.rect.x < 0 - self.rect.width:
            self.kill()
            return self.missReturn

        if self.checkCollisions(points):
            self.ding_sound.play()
            return self.abort()

    def abort(self):
        self.kill()
        return True

    def checkCollisions(self, points):
        for i in range(len(points)-1):
            if self.rect.collidepoint((int((1-points[i][0])*self.windowWidth),int(points[i][1]*self.windowHeight))):
                if checkVelocity(points[4][i]):
                    return True
        return False
    

class bomb(fruit):
    def __init__(self, windowWidth, windowHeight):
        super().__init__(windowWidth, windowHeight)

        self.image = pygame.image.load("Fruit_images/Bomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (170, 170))

        self.ding_sound = pygame.mixer.Sound('Sounds/bomb_noise.mp3')

        self.missReturn = "bomb-miss"

    def abort(self):
        self.kill()
        return "bomb"


def checkVelocity(points):
    point1 = np.array([points[0][0], points[0][1]])
    point2 = np.array([points[1][0], points[1][1]])
    distance = np.linalg.norm(point2 - point1)
    if distance >= 0.17:
        return True
    return False