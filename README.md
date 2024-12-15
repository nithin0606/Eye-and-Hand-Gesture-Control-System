# Eye-and-Hand-Gesture-Control-System

This project combines computer vision and machine learning to implement an interactive system that allows users to control a virtual mouse using eye-tracking and hand gestures. The system leverages Mediapipe for landmark detection and PyAutoGUI for cursor control, providing a seamless, touch-free interaction experience.

Features
Eye Control:

Move the cursor by tracking eye movement.
Perform left and right clicks with blinks.
Hand Gesture Control:

Navigate and click using intuitive hand gestures.
Detect raised fingers to interpret specific actions.
Dynamic Adaptation:

Automatically adjusts to screen dimensions for precise control.
Real-time tracking with FPS monitoring for smooth performance.
Technologies Used
Programming Language: Python
Libraries:
OpenCV: For image processing and video frame manipulation.
Mediapipe: For face and hand landmark detection.
PyAutoGUI: For controlling mouse and keyboard events.
Time: For performance and FPS monitoring.

Setup and Installation

Clone the repository to your local machine.

git clone <repository_url>
cd <repository_directory>
Install the required Python libraries.
 
pip install opencv-python mediapipe pyautogui
Run the scripts for eye or hand control:

For eye-based cursor control:
 
python eye.py  

For hand-based cursor control:

python hand.py  
Usage
Eye Gesture Control:

Ensure your webcam is active and positioned properly.
Use your eyes to move the cursor, and blink for clicks.
Hand Gesture Control:

Show your hand clearly in front of the camera.
Raise fingers to move the cursor or perform clicks based on detected gestures.
Applications
Accessibility tool for users with limited mobility.
Contactless control systems for hygiene-sensitive environments.
Educational and interactive demonstrations of computer vision.

Support
If you encounter any issues or have questions, feel free to reach out via email at nithinm089@gmail.com
