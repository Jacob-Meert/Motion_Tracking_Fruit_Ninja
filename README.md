# Motion Ninja Game

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/Pygame-2.1.0-green.svg)](https://www.pygame.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5.0-red.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8.9-orange.svg)](https://mediapipe.dev/)

A motion-controlled Fruit Ninja style game that uses your webcam and body movements to slice fruits!

![Motion Ninja Game](https://via.placeholder.com/800x400?text=Motion+Ninja+Game)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Controls](#game-controls)
- [Files in the Project](#files-in-the-project)
- [Difficulty Modes](#difficulty-modes)
- [Game Elements](#game-elements)
- [Development Notes](#development-notes)
- [Future Improvements](#future-improvements)

## 🔍 Overview

Motion Ninja is a camera-based game inspired by Fruit Ninja, where players use their body movements to slice virtual fruits that appear on the screen. The game uses computer vision and pose detection technology to track your hands and feet, allowing you to interact with the game objects without touching the screen or using traditional controllers.

## ✨ Features

- **Full-body motion controls**: Use your hands and feet to slice fruits
- **Real-time pose detection**: Tracks your movements using your webcam
- **Multiple difficulty levels**: Choose between normal and hard modes
- **Visual feedback**: Colorful trails follow your movements
- **Score tracking**: Keep track of your current score and high score
- **Lives system**: Three chances before game over
- **Bomb obstacles**: Avoid slicing bombs or lose immediately
- **Dynamic difficulty**: Game gets faster as you play longer

## 🔧 Requirements

- Python 3.6 or higher
- Webcam
- Sufficient space to move freely
- Good lighting conditions

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/motion-ninja.git
   cd motion-ninja
   ```

2. Install the required dependencies:
   ```bash
   pip install pygame opencv-python mediapipe numpy
   ```

3. Make sure you have the necessary folders and assets:
   - `Fruit_images/` folder containing all fruit and button images
   - `Sounds/` folder containing game audio files

4. Run the game:
   ```bash
   python GameOverlay.py
   ```

## 📝 How to Play

1. Start the game and stand in front of your webcam where your full body is visible
2. Choose your difficulty level by hovering your hand over the Normal or Hard button for 2 seconds
3. Press the Start button by hovering your hand over it for 2 seconds
4. Fruits will start appearing from the bottom of the screen
5. Move your hands and feet quickly to slice the fruits
6. Avoid slicing bombs (black spheres) or you'll lose immediately
7. You have 3 lives - each missed fruit costs 1 life
8. Try to achieve the highest score possible!

## 🎮 Game Controls

| Action | Control |
|--------|---------|
| Select option | Hover hand over button for 2 seconds |
| Slice fruit | Move hands or feet through fruit with sufficient velocity |
| Exit game | Press SPACEBAR |

## 📁 Files in the Project

| File | Description |
|------|-------------|
| `GameOverlay.py` | Main game file with the camera interface and game logic |
| `FruitNinja.py` | Contains sprite classes for fruits, bombs, and limb tracking |
| `Fruit_images/` | Directory containing all game images and buttons |
| `Sounds/` | Directory containing game sound effects |

## 🎚️ Difficulty Modes

### Normal Mode
- Initial spawn interval: 2.5 seconds
- Minimum spawn interval: 0.7 seconds
- Difficulty increases gradually

### Hard Mode
- Initial spawn interval: 1.5 seconds
- Minimum spawn interval: 0.3 seconds
- Difficulty increases more rapidly

## 🍎 Game Elements

### Fruits
Various fruits will appear from the bottom of the screen and follow an arc trajectory. Slice them by moving your hands or feet through them with sufficient velocity.

### Bombs
Black spheres that appear randomly. Avoid slicing them or the game will end immediately regardless of remaining lives.

### Lives
You start with 3 lives. Each missed fruit costs 1 life. When all lives are lost, the game ends.

### Score
Each successfully sliced fruit earns you 100 points. Try to achieve the highest score possible!

## 💻 Development Notes

The game uses:
- **Pygame** for game rendering and physics
- **OpenCV** for camera capture and processing
- **MediaPipe** for pose detection and tracking
- **NumPy** for mathematical calculations

The motion detection works by:
1. Capturing video from the webcam
2. Processing each frame to detect body pose using MediaPipe
3. Tracking the position of hands and feet
4. Calculating velocity between frames to determine slicing motion
5. Checking collisions between limb positions and fruit sprites

```
┌─────────────┐    ┌───────────────┐    ┌────────────────┐
│  Camera     │───►│ Pose Detection │───►│ Position       │
│  Input      │    │ (MediaPipe)    │    │ Tracking       │
└─────────────┘    └───────────────┘    └────────┬───────┘
                                                 │
                                                 ▼
┌─────────────┐    ┌───────────────┐    ┌────────────────┐
│  Game       │◄───│ Collision     │◄───│ Velocity       │
│  Rendering  │    │ Detection     │    │ Calculation    │
└─────────────┘    └───────────────┘    └────────────────┘
```

## 🔮 Future Improvements

- [ ] Add more fruit varieties with different point values
- [ ] Implement special power-up fruits
- [ ] Add multiplayer support for competitive play
- [ ] Create a tutorial mode for beginners
- [ ] Add customizable backgrounds and visual themes
- [ ] Implement different game modes (time attack, zen mode, etc.)
- [ ] Support for recording and sharing gameplay highlights

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
