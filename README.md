# Hand Gesture Recognition and Virtual Mouse Control

A real-time human-computer interaction application that recognizes hand gestures from webcam input and converts selected gestures into mouse-control operations. The system uses MediaPipe to detect hand landmarks, OpenCV and NumPy for gesture analysis, and PyQt5 to provide a graphical user interface.

## Features

- Detects up to two hands simultaneously from live webcam input.
- Identifies 21 landmarks for each detected hand using MediaPipe.
- Recognizes 12 numerical and symbolic gestures using a convex-hull-based method and landmark geometry.
- Maps selected gestures to touch-free mouse controls.
- Applies coordinate interpolation and motion smoothing for responsive cursor movement.
- Displays the live camera feed, hand landmarks, handedness, and recognition results in a custom PyQt5 interface.
- Provides separate modes for gesture recognition and mouse control.

## Supported Gestures

The recognition mode supports the following 12 gestures:

`0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `ROCK`, and `LOVE`

## Mouse Controls

In mouse-control mode, recognized gestures are mapped to the following operations:

| Gesture | Mouse operation |
| --- | --- |
| `1` | Move the cursor with the index finger |
| `2` | Left-click |
| `3` | Right-click |
| `4` | Double-click |
| `0` | Scroll down |
| `5` | Scroll up |

Scrolling up and down are treated as one mouse-control category. Click gestures are triggered when the gesture changes, helping prevent repeated clicks across consecutive video frames.

## Technologies

- Python
- MediaPipe
- OpenCV
- NumPy
- PyQt5
- AutoPy
- PyAutoGUI

## Project Structure

```text
Hand_MediaPipe/
├── Hand_Wang.py       # Hand tracking, gesture recognition, and mouse control
├── My_gui.py          # PyQt5 interface generated from the UI definition
├── My_gui.ui          # Qt Designer interface file
├── requirements.txt   # Python dependencies
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Hand_MediaPipe
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the application from the project directory:

```bash
python Hand_Wang.py
```

After the interface opens:

1. Select **Gesture** to recognize and display hand gestures.
2. Select **Mouse** to control the mouse using the supported gestures.
3. Keep your hand visible to the webcam and use a well-lit background for more reliable tracking.

The application requests access to the default webcam. Depending on the operating system, it may also require accessibility or input-control permission to perform mouse operations.

## How It Works

1. OpenCV captures frames from the webcam.
2. MediaPipe detects each hand and returns 21 normalized landmark coordinates.
3. The coordinates are converted into image-space points.
4. A convex hull and landmark relationships are used to identify raised fingers and classify the gesture.
5. In mouse-control mode, the recognized gesture triggers its assigned operation through AutoPy or PyAutoGUI.
6. Cursor coordinates are mapped from the camera frame to the screen and smoothed to reduce abrupt movement.

## Notes

- A working webcam is required.
- Recognition quality depends on lighting, hand visibility, and camera position.
- The application is configured to use the system's default camera.
- The graphical interface was designed for a large display area and may require layout adjustment on smaller screens.
