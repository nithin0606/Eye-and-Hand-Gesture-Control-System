import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize webcam, hand detector, and screen dimensions
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# FPS monitoring
prev_time = 0

# Function to detect raised fingers
def detect_fingers_status(landmarks):
    fingers = []
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)  # Thumb is up
    else:
        fingers.append(0)  # Thumb is down

    finger_tips = [8, 12, 16, 20]
    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)  # Finger is up
        else:
            fingers.append(0)  # Finger is down
    return fingers

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Drawing landmarks only for debugging
            # drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            index_finger_tip = landmarks[8]
            index_x = int(index_finger_tip.x * screen_width)
            index_y = int(index_finger_tip.y * screen_height)

            fingers = detect_fingers_status(landmarks)

            if fingers[1] == 1 and sum(fingers) > 1:
                smoothed_x = int(0.7 * pyautogui.position().x + 0.3 * index_x)
                smoothed_y = int(0.7 * pyautogui.position().y + 0.3 * index_y)
                pyautogui.moveTo(smoothed_x, smoothed_y)
                cv2.putText(frame, "Cursor Moving", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif fingers[1] == 0 and fingers[2] == 1:
                pyautogui.click(button='left')
                cv2.putText(frame, "Left Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                pyautogui.sleep(0.1)

            elif fingers[1] == 1 and fingers[2] == 0:
                pyautogui.click(button='right')
                cv2.putText(frame, "Right Click", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                pyautogui.sleep(0.1)

    # FPS display
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Virtual Mouse', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
