import cv2
import numpy as np

def preprocess_image(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply morphological opening to remove noise and small objects
    kernel = np.ones((2, 2), np.uint8)  # Smaller kernel for opening
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)

    return opened

def detect_cars(frame):
    # Preprocess the frame to enhance contours
    processed_frame = preprocess_image(frame)

    # Apply edge detection (Canny)
    edges = cv2.Canny(processed_frame, 80, 200)

    # Find contours
    adaptive_thresh = cv2.adaptiveThreshold(processed_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and shape
    min_area = 12000
    max_area = 18000
    cars = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            # Append detected car bounding box
            cars.append((x, y, w, h))

    return cars, edges

def process_video(video_path, skip_frames=3):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frames by checking if the current frame count is divisible by the skip rate
        if frame_count % skip_frames != 0:
            continue

        # Detect cars in the frame and get debug images
        cars, edges = detect_cars(frame)

        # Draw rectangles around detected cars
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle

        # Display all debugging windows
        cv2.imshow('Original', frame)
        cv2.imshow('Edges', edges)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything
    cap.release()
    cv2.destroyAllWindows()

# Use the script
if __name__ == "__main__":
    video_path = "../data/2/PARKING.mov"
    process_video(video_path, skip_frames=3)
