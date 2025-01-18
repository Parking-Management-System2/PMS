import cv2

def detect_cars(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply threshold to get binary image - inverted threshold for bright objects
    _, thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)  # Changed from THRESH_BINARY_INV

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_area = 500  # Adjust this value based on your video
    max_area = 5000  # Adjust this value based on your video

    cars = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            # Filter based on aspect ratio
            aspect_ratio = w / float(h)
            if 0.5 < aspect_ratio < 2.0:  # Adjust these values based on your cars
                cars.append((x, y, w, h))

    return cars, gray, thresh


def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect cars in the frame and get debug images
        cars, gray, thresh = detect_cars(frame)

        # Draw rectangles around detected cars
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle

        # Display all debugging windows
        cv2.imshow('Original', frame)
        cv2.imshow('Threshold', thresh)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything
    cap.release()
    cv2.destroyAllWindows()


# Use the script
if __name__ == "__main__":
    video_path = "../data/PARKING4.mp4"
    process_video(video_path)