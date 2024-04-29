import streamlit as st
from cvzone.FaceDetectionModule import FaceDetector
import cv2
import cvzone

st.set_page_config(page_title="Computer Vision")

operations = ['Hand Detect', 'Face Detection']
st.selectbox("Chosse the Operation", operations)


img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as bytes:
    bytes_data = img_file_buffer.getvalue()
    # Check the type of bytes_data:
    # Should output: <class 'bytes'>
    st.write(type(bytes_data))

detector = FaceDetector()

# Load the image to overlay on detected faces
img_overlay = cv2.imread('./sources/sample.png', cv2.IMREAD_UNCHANGED)



# Start capturing video from the webcam
cap = cv2.VideoCapture(0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces in the frame
    frame, faces = detector.findFaces(frame)

    # Iterate over detected faces
    if faces:
        for face in faces:
            # Get the bounding box coordinates of the face
            x, y, w, h = face['bbox']

            # Overlay the image on the detected face
            frame = cvzone.overlayPNG(frame, img_overlay, [x, y, w, h])

    # Display the resulting frame
    cv2.imshow('Face Detection with Overlay', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()