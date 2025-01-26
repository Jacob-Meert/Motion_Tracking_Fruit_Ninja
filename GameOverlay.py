import pygame
import cv2
import numpy as np
import random
import time
import FruitNinja
import mediapipe as mp

mp_pose = mp.solutions.pose


def launchGame():
    sprites = pygame.sprite.Group()
    last_spawn_time = 0  # Track when the last fruit was spawned
    initial_spawn_interval = 2.5
    spawn_interval = initial_spawn_interval  # Spawn fruit every 2 seconds
    min_spawn_interval = 0.5  # Minimum spawn interval
    game_start_time = time.time()
    
    def calculate_spawn_interval():
        elapsed_time = time.time() - game_start_time
        return max(initial_spawn_interval - (elapsed_time // 30) * 0.2, min_spawn_interval)
    
    # Initialize game and window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Motion-Box")

    
    #create start button
    startButton = Button(
        screen.get_width() // 2 - screen.get_width() // 8,
        screen.get_height() // 2,
        screen.get_width() // 4,
        screen.get_height() // 6,
        'start.png',
    )

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    rightHandTracker = FruitNinja.limbTracker(screen.get_width(), screen.get_height())
    leftHandTracker = FruitNinja.limbTracker(screen.get_width(), screen.get_height())
    rightFootTracker = FruitNinja.limbTracker(screen.get_width(), screen.get_height())
    leftFootTracker = FruitNinja.limbTracker(screen.get_width(), screen.get_height())

    Clock = pygame.time.Clock()

    gameStart = False
    running = True

    hold_start_time = None
    hold_duration = 2

    score = 0
    lives = 3

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    running = False

            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read from the camera")
                break

            # Convert image from BGR to RGB because pygame uses RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Perform pose detection
            results = pose.process(image)

            # Convert image back to BGR
            image.flags.writeable = True
            
            # Flip image horizontally and convert for Pygame
            image = cv2.flip(np.transpose(image, (1, 0, 2)), 0)
            frame_surface = pygame.surfarray.make_surface(image)
            frame_surface = pygame.transform.scale(frame_surface, (screen.get_width(), screen.get_height()))
            screen.blit(frame_surface, (0, 0))

            # Track right hand
            if results.pose_landmarks:
                right_hand_pos = getRightHandCoordinates(results.pose_landmarks.landmark)
                rightHandTracker.update(right_hand_pos)
                rightHandTracker.draw(screen)

                left_hand_pos = getLeftHandCoordinates(results.pose_landmarks.landmark)
                leftHandTracker.update(left_hand_pos)
                leftHandTracker.draw(screen)

                right_foot_pos = getRightFootCoordinates(results.pose_landmarks.landmark)
                rightFootTracker.update(right_foot_pos)
                rightFootTracker.draw(screen)

                left_foot_pos = getLeftFootCoordinates(results.pose_landmarks.landmark)
                leftFootTracker.update(left_foot_pos)
                leftFootTracker.draw(screen)


                hand_screen_pos = (
                    int((1 - right_hand_pos[0]) * screen.get_width()),
                    int(right_hand_pos[1] * screen.get_height()),
                )


            if not gameStart:
                startButton.draw(screen)

                if results.pose_landmarks and startButton.is_hand_over(hand_screen_pos):
                    if hold_start_time is None:
                        hold_start_time = time.time()  # Start the timer
                    elif time.time() - hold_start_time >= hold_duration:
                        gameStart = True  # Start the game
                        hold_start_time = None  # Reset the timer
                else:
                    hold_start_time = None  # Reset the timer if the hand moves away
            spawn_interval = calculate_spawn_interval()

            # Start spawning fruits when the game starts
            if gameStart:
                current_time = time.time()
                if current_time - last_spawn_time > spawn_interval:
                    fruit = FruitNinja.fruit(screen.get_width(), screen.get_height())
                    sprites.add(fruit)
                    last_spawn_time = current_time

            # Ensure pose landmarks are available before calling coordinate functions
            if results.pose_landmarks:
                left_hand = getLeftHandCoordinates(results.pose_landmarks.landmark)
                right_hand = getRightHandCoordinates(results.pose_landmarks.landmark)
                left_foot = getLeftFootCoordinates(results.pose_landmarks.landmark)
                right_foot = getRightFootCoordinates(results.pose_landmarks.landmark)
            else:
                # Provide fallback values if landmarks are not detected
                left_hand = (0, 0, 0)
                right_hand = (0, 0, 0)
                left_foot = (0, 0, 0)
                right_foot = (0, 0, 0)

            # Update sprites at each tick
            for sprite in sprites:
                curr = sprite.update([left_hand, right_hand, left_foot, right_foot])
                if curr == True:
                    score += 100
                elif curr == False:
                    lives -= 1
                    if lives <= 0:
                        gameStart = False
                        for sprite in sprites:
                            sprite.abort()
                        lives =3

            sprites.draw(screen)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            Clock.tick(100)

        cap.release()
        pygame.quit()



def getRightHandCoordinates(landmarks):
    finger = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value]
    return (finger.x, finger.y, finger.z)


def getLeftHandCoordinates(landmarks):
    finger = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value]
    return (finger.x, finger.y, finger.z)


def getRightFootCoordinates(landmarks):
    foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
    return (foot.x, foot.y, foot.z)


def getLeftFootCoordinates(landmarks):
    foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
    return (foot.x, foot.y, foot.z)


class Button:
    def __init__(self, x, y, width, height, imageName):
        self.image = pygame.image.load("Fruit_images/" + imageName).convert_alpha()  # Load image with transparency
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_hand_over(self, hand_pos):
        return self.rect.collidepoint(hand_pos)


launchGame()