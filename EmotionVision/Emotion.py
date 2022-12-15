import torch
from torchvision import transforms
import cv2

print(cv2.__version__)
# Load the pre-trained model
model = torch.load('emotion_detection_model.pt')

# Set up the camera
camera = cv2.VideoCapture(0)

# Loop indefinitely
while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Preprocess the frame
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    frame_tensor = transform(frame).unsqueeze(0)

    # Run the model on the frame and get the predicted emotions
    output = model(frame_tensor)
    emotions = output.argmax(dim=1)

    # Display the frame and the predicted emotions
    cv2.imshow('Frame', frame)
    print('Emotions:', emotions)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()
