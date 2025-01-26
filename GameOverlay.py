import pygame
import cv2
import numpy as np
import random
import time
import FruitNinja
import mediapipe as mp

mp_pose = mp.solutions.pose


def launchGame():
    # Difficulty configurations
    DIFFICULTY_SETTINGS = {
        1: {  # Normal mode
            "initial_spawn_interval": 2.5,
            "min_spawn_interval": .7,
            "speed_of_change": 0.2  # How much spawn interval decreases every 30 seconds
        },
        2: {  # Hard mode
            "initial_spawn_interval": 1.5,
            "min_spawn_interval": 0.3,
            "speed_of_change": 0.3
        }
    }
    difficulty = None
    initial_spawn_interval = 2.5
    min_spawn_interval = 0.5
    speed_of_change = 0.2

    remove = False
    velocityTrackRH = queue(coord(None))
    velocityTrackRF = queue(coord(None))
    velocityTrackLH = queue(coord(None))
    velocityTrackLF = queue(coord(None))
    sprites = pygame.sprite.Group()
    last_spawn_time = 0  # Track when the last fruit was spawned
    initial_spawn_interval = 2.5
    spawn_interval = initial_spawn_interval  # Spawn fruit every 2 seconds
    min_spawn_interval = 0.5  # Minimum spawn interval
    game_start_time = time.time()
    difficulty = None

    
    lastTrack = 0
    
    def calculate_spawn_interval():
        elapsed_time = time.time() - game_start_time
        return max(initial_spawn_interval - (elapsed_time // 30) * speed_of_change, min_spawn_interval)
    
    # Initialize game and window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Motion-Box")

    
    #create start button
    startButton = Button(
        screen.get_width() // 2 - screen.get_width() // 8,
        screen.get_height() - screen.get_height() // 3,
        screen.get_width() // 4,
        screen.get_height() // 6,
        'start.png',
        'start_pressed.png'
    )
    normalButton = Button(
        screen.get_width() - 4*(screen.get_width() // 5),
        screen.get_height() - 1.7*(screen.get_height() //3),
        screen.get_width() // 4,
        screen.get_height() // 6,
        'normal.png',
        'normal_pressed.png'
    )
    hardButton = Button(
        screen.get_width() - 2.3*(screen.get_width() // 5),
        screen.get_height() - 1.7*(screen.get_height() //3),
        screen.get_width() // 4,
        screen.get_height() // 6,
        'hard.png',
        'hard_pressed.png'
    )


    cap = cv2.VideoCapture(0)

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
    normal_held = True
    hard_held = False

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
            else:
                hand_screen_pos = (0,0)


            if not gameStart:
                normalButton.set_pressed(normal_held)
                hardButton.set_pressed(hard_held)
                
                startButton.draw(screen, hand_screen_pos)
                normalButton.draw(screen,hand_screen_pos)
                hardButton.draw(screen,hand_screen_pos)

                if results.pose_landmarks and normalButton.is_hand_over(hand_screen_pos):
                    if hold_start_time is None:
                        hold_start_time = time.time()  # Start the timer
                    elif time.time() - hold_start_time >= hold_duration:
                        normal_held = True  
                        hard_held = False
                        difficulty = 1 #Normal mode
                        hold_start_time = None  # Reset the timer
                elif results.pose_landmarks and hardButton.is_hand_over(hand_screen_pos):
                    if hold_start_time is None:
                        hold_start_time = time.time()  # Start the timer
                    elif time.time() - hold_start_time >= hold_duration:
                        hard_held = True  
                        normal_held = False
                        difficulty = 2 #hard mode
                        hold_start_time = None  # Reset the timer
                elif results.pose_landmarks and startButton.is_hand_over(hand_screen_pos): 
                    if hold_start_time is None:
                        hold_start_time = time.time()  # Start the timer
                    elif time.time() - hold_start_time >= hold_duration:
                        gameStart = True  # Start the game
                        hold_start_time = None  # Reset the timer
                else:
                    hold_start_time = None  # Reset the timer if the hand moves away
            

            # Start spawning fruits when the game starts
            if gameStart:
                if normal_held and difficulty == 1:
                    settings = DIFFICULTY_SETTINGS[1]
                elif hard_held and difficulty == 2:
                    settings = DIFFICULTY_SETTINGS[2]

                # Apply settings dynamically based on selected difficulty
                initial_spawn_interval = settings["initial_spawn_interval"]
                min_spawn_interval = settings["min_spawn_interval"]
                speed_of_change = settings["speed_of_change"]

                # Recalculate the spawn interval dynamically
                spawn_interval = calculate_spawn_interval()
                
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


                if pygame.time.get_ticks() >= lastTrack + 1:
                    lastTrack == pygame.time.get_ticks()
                    velocityTrackRH.add(coord(right_hand))
                    velocityTrackRF.add(coord(right_foot))
                    velocityTrackLH.add(coord(left_hand))
                    velocityTrackLF.add(coord(left_foot))

                    if remove == False:
                        if len(velocityTrackLF) >= 10:
                            remove = True
                    else:
                        velocityTrackRH.pop()
                        velocityTrackRF.pop()
                        velocityTrackLH.pop()
                        velocityTrackLF.pop()
            else:
                # Provide fallback values if landmarks are not detected
                left_hand = (0, 0, 0)
                right_hand = (0, 0, 0)
                left_foot = (0, 0, 0) 
                right_foot = (0, 0, 0)

            # Update sprites at each tick
            for sprite in sprites:
                curr = sprite.update([left_hand, right_hand, left_foot, right_foot,[(velocityTrackLH.head.value,velocityTrackLH.tail.value) , (velocityTrackRH.head.value,velocityTrackRH.tail.value), (velocityTrackLF.head.value,velocityTrackLF.tail.value), (velocityTrackRF.head.value,velocityTrackRF.tail.value)]])
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
    def __init__(self, x, y, width, height, default_image, hover_image):
        # Load default and hover images
        self.default_image = pygame.image.load("Fruit_images/" + default_image).convert_alpha()
        self.default_image = pygame.transform.scale(self.default_image, (width, height))
        
        self.hover_image = pygame.image.load("Fruit_images/" + hover_image).convert_alpha()
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        
        self.image = self.default_image  # Set the default image initially
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False

    def draw(self, screen, hand_pos):
        # Switch to hover image if hand is over the button or if it's pressed
        if self.pressed or self.is_hand_over(hand_pos):
            self.image = self.hover_image
        else:
            self.image = self.default_image

        # Draw the current image
        screen.blit(self.image, self.rect)

    def is_hand_over(self, hand_pos):
        return self.rect.collidepoint(hand_pos)
    
    def set_pressed(self, pressed):
        self.pressed = pressed
        
class queue:
    def __init__(self, head):
        self.head = head
        self.tail = head
    
    def pop(self):
        self.head = self.head.next

    def add(self, node):
        self.tail.next = node
        self.tail = node

    def __len__(self):
        current = self.head
        count = 0
        while current:
            current = current.next
            count += 1
        return count
    
    def __str__(self):
        current = self.head
        string = 'Begin -- \n'
        while current:
            string += str(current.value) + " -> "
            current = current.next
        return string

    def __repr__(self):
        return self.__str__()


class coord:
    def __init__(self, value, next = None):
        self.value = value
        self.next = next

launchGame()