import cv2
import os
from datetime import datetime

# Initialize global variables for video capture and writer
video_writer = None
video_filename = None
video_capture = None

def Process(input_filepath):
    global video_writer, video_filename, video_capture

    # Set up the video capture from the file
    video_capture = cv2.VideoCapture(input_filepath)

    # Check if the video capture was initialized successfully
    if not video_capture.isOpened():
        print("Error: Could not open video capture device.")
        return

    # Set up the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error loading Haar cascade")
        return

    # Generate a dynamic filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f'processed_{timestamp}.avi'

    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)

    # Define the video writer object
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video_writer = cv2.VideoWriter(os.path.join('uploads', video_filename), fourcc, 24, (640, 480))

    # Variables for motion detection
    ret, frame1 = video_capture.read()
    if not ret or frame1 is None:
        print("Error: Could not read frame1 from video capture.")
        release_resources()
        return
    
    ret, frame2 = video_capture.read()
    if not ret or frame2 is None:
        print("Error: Could not read frame2 from video capture.")
        release_resources()
        return

    motion_detected = False

    while True:
        if frame1 is None or frame2 is None:
            print("Error: One of the frames is None.")
            break
        
        # Ensure both frames have the same size and number of channels
        if frame1.shape != frame2.shape:
            print("Error: Frame sizes do not match.")
            break

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True

        if motion_detected:
            # Write the frame to the video writer
            video_writer.write(frame1)
            motion_detected = False

        frame1 = frame2
        ret, frame2 = video_capture.read()
        if not ret:
            break

    release_resources()

def release_resources():
    global video_writer, video_capture

    if video_capture is not None:
        video_capture.release()

    if video_writer is not None:
        video_writer.release()
        video_writer = None
