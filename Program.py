import cv2
import os
from datetime import datetime

# Initialize global variables for video capture and writer
video_capture = None
video_writer = None
video_filename = None

def Process():
    global video_capture, video_writer, video_filename

    # Set up the video capture
    video_capture = cv2.VideoCapture(0)

    # Set up the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Error loading Haar cascade")

    # Generate a dynamic filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f'video_{timestamp}.avi'

    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)

    # Define the video writer object
    video_writer = cv2.VideoWriter(os.path.join('uploads', video_filename), cv2.VideoWriter_fourcc(*"MJPG"), 24, (640, 480))

    while True:
        # Capture a frame from the video
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Write the frame to the video writer
        video_writer.write(frame)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Check for user input and break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and writer
    release_resources()

def stop_process():
    release_resources()

def release_resources():
    global video_capture, video_writer

    if video_capture is not None:
        video_capture.release()
        video_capture = None

    if video_writer is not None:
        video_writer.release()
        video_writer = None

    cv2.destroyAllWindows()
