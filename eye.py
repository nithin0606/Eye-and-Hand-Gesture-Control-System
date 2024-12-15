import cv2
import mediapipe as mp
import pyautogui

# Initialize webcam and Mediapipe Face Mesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()  # Get screen size for cursor mapping

while True:
    # Read frame from webcam
    ret, frame = cam.read()
    if not ret:
        break

    # Flip the frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect face landmarks
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        # Get landmarks for the first detected face
        landmarks = landmark_points[0].landmark

        # Cursor movement using eye landmarks (landmarks 474-478)
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Visualize eye landmarks
            if id == 1:  # Map a specific landmark to mouse movement
                screen_x = int(landmark.x * screen_w)
                screen_y = int(landmark.y * screen_h)
                pyautogui.moveTo(screen_x, screen_y, duration=0.05)

        # Blink detection for LEFT eye (landmarks 145 and 159)
        left_eye_top = landmarks[145]
        left_eye_bottom = landmarks[159]
        left_eye_left_corner = landmarks[33]
        left_eye_right_corner = landmarks[133]

        # Calculate distances for left eye
        left_top_y = left_eye_top.y * frame_h
        left_bottom_y = left_eye_bottom.y * frame_h
        left_eye_height = abs(left_top_y - left_bottom_y)

        left_eye_width = abs(left_eye_left_corner.x - left_eye_right_corner.x) * frame_w
        left_blink_threshold = left_eye_width * 0.2  # Dynamic threshold for blinking

        # Visualize blink detection points for left eye
        for landmark in [left_eye_top, left_eye_bottom]:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        # Check for left eye blink
        if left_eye_height < left_blink_threshold:
            pyautogui.click(button='left')
            pyautogui.sleep(0.5)  # Prevent multiple clicks in quick succession

        # Blink detection for RIGHT eye (landmarks 374 and 386)
        right_eye_top = landmarks[374]
        right_eye_bottom = landmarks[386]
        right_eye_left_corner = landmarks[362]
        right_eye_right_corner = landmarks[263]

        # Calculate distances for right eye
        right_top_y = right_eye_top.y * frame_h
        right_bottom_y = right_eye_bottom.y * frame_h
        right_eye_height = abs(right_top_y - right_bottom_y)

        right_eye_width = abs(right_eye_left_corner.x - right_eye_right_corner.x) * frame_w
        right_blink_threshold = right_eye_width * 0.2  # Dynamic threshold for blinking

        # Visualize blink detection points for right eye
        for landmark in [right_eye_top, right_eye_bottom]:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)

        # Check for right eye blink
        if right_eye_height < right_blink_threshold:
            pyautogui.click(button='right')
            pyautogui.sleep(0.5)  # Prevent multiple clicks in quick succession

    # Display the frame with visual annotations
    cv2.imshow('Eye Controlled Mouse', frame)

    # Exit on pressing 'q' or 'ESC'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 'q' or ESC key
        break

# Release resources
cam.release()
cv2.destroyAllWindows()
