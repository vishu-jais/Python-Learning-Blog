import cv2

# Load the pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam (use 0 for default camera)
cap = cv2.VideoCapture(0)

print("🔍 Press 'q' to quit the face detection window")

while True:
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to access camera")
        break

    # Convert frame to grayscale (faster processing)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,     # Adjust detection accuracy
        minNeighbors=5,      # Reduce false positives
        minSize=(30, 30)
    )

    # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, "Face", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the output
    cv2.imshow('Face Detection', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
