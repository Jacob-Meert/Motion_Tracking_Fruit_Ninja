# 🥷 Motion Tracking Fruit Ninja

A real-time, motion-controlled version of the classic Fruit Ninja game, played using body movements tracked through your webcam! Slice flying fruit by swinging your arms or kicking in the air — no mouse or keyboard required.

## 🎮 Features

- **Real-time gameplay** powered by OpenCV and PyGame
- **Full-body interaction** using MediaPipe for motion tracking
- **Custom game overlay system** for UI rendering and fruit animations
- **Scalable difficulty** that adapts as you play
- **Dynamic slicing detection** with limb tracking and collision logic
- Modular codebase: separated logic for core game loop and overlay

## 🧠 Tech Stack

- **Python**
- **MediaPipe** (for motion tracking)
- **PyGame** (for rendering and game loop)
- **NumPy** (for fast array/math operations)
- **OpenCV** (for webcam and image manipulation)

## 🚀 How It Works

1. **Player Detection:**  
   MediaPipe uses your webcam to detect and track key body landmarks (hands, elbows, knees).

2. **Gesture Recognition:**  
   Swinging your arms or kicking sends tracked keypoints into a real-time collision system.

3. **Fruit Spawning & Slicing:**  
   Fruits spawn and fall with randomized paths. If a tracked body part intersects with a fruit’s path, the fruit is "sliced".

4. **Game Overlay:**  
   `GameOverlay.py` manages drawing, fonts, animations, and UI layout for lives, score, and game status.

## 📝 How to Run

1. **Install Requirements**

   ```bash
   pip install mediapipe opencv-python pygame numpy
