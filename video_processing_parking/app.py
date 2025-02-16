import sys
import os
import cv2
import numpy as np

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.car_data import CarData
from redis_db.parking_gate_data import ParkingGateData

# Constants for car detection parameters
GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
MORPH_OPEN_KERNEL_SIZE = (2, 2)
CANNY_EDGE_THRESHOLD1 = 80
CANNY_EDGE_THRESHOLD2 = 200
ADAPTIVE_THRESH_BLOCK_SIZE = 11
ADAPTIVE_THRESH_C = 2
MIN_CAR_CONTOUR_AREA = 12000
MAX_CAR_CONTOUR_AREA = 18000

# Constants for parking slot detection parameters
MIN_PARKING_SLOT_CONTOUR_AREA = 22000
MAX_PARKING_SLOT_CONTOUR_AREA = 38000

SKIP_FRAMES = 3
VIDEO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '2', 'PARKING.MOV'))
MAX_UNDETECTED_FRAMES = 250  # Maximum number of frames a car can be undetected before being removed

def preprocess_image(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, GAUSSIAN_BLUR_KERNEL_SIZE, 0)

    # Apply morphological opening to remove noise and small objects
    kernel = np.ones(MORPH_OPEN_KERNEL_SIZE, np.uint8)  # Smaller kernel for opening
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, kernel)

    return opened

def detect_objects(frame):
    # Preprocess the frame to enhance contours
    processed_frame = preprocess_image(frame)

    # Apply edge detection (Canny)
    edges = cv2.Canny(processed_frame, CANNY_EDGE_THRESHOLD1, CANNY_EDGE_THRESHOLD2)

    # Find contours
    adaptive_thresh = cv2.adaptiveThreshold(processed_frame, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_C)
    contours, _ = cv2.findContours(adaptive_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and shape
    cars = []
    parking_slots = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if MIN_CAR_CONTOUR_AREA < area < MAX_CAR_CONTOUR_AREA:
            # Get bounding rectangle for cars
            x, y, w, h = cv2.boundingRect(contour)
            cars.append((x, y, w, h))
        elif MIN_PARKING_SLOT_CONTOUR_AREA < area < MAX_PARKING_SLOT_CONTOUR_AREA:
            # Get bounding rectangle for parking slots
            x, y, w, h = cv2.boundingRect(contour)
            parking_slots.append((x, y, w, h))

    return cars, parking_slots, edges

def process_video(video_path, skip_frames=SKIP_FRAMES, car_data=None, parking_gate_data=None):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    if car_data is None:
        car_data = CarData()

    if parking_gate_data is None:
        parking_gate_data = ParkingGateData()    

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break

        # Rotate the frame by 90 degrees
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        frame_count += 1

        # Skip frames by checking if the current frame count is divisible by the skip rate
        if frame_count % skip_frames != 0:
            continue

        # Detect cars and parking slots in the frame and get debug images
        cars, parking_slots, edges = detect_objects(frame)
        car_data.update_cars(cars, frame_count, MAX_UNDETECTED_FRAMES)

        # Draw rectangles around detected cars
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle for cars

        # Draw rectangles around detected parking slots
        for (x, y, w, h) in parking_slots:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green rectangle for parking slots

        # Draw a blue rectangle in the upper right corner
        height, width, _ = frame.shape
        upper_left_x = int(width * 2.5 / 4)
        upper_left_y = int(height * 0.6 / 4)
        bottom_right_x = width
        bottom_right_y = int(height * 2 / 4)
        cv2.rectangle(frame, (upper_left_x, upper_left_y), (bottom_right_x, bottom_right_y), (255, 0, 0), 2)  # Blue rectangle

        # Check if a car is located in the blue rectangle and if so update its status and position
        car_in_blue_rectangle = None
        for (x, y, w, h) in cars:
            if upper_left_x <= x <= bottom_right_x and upper_left_y <= y <= bottom_right_y:
                car_in_blue_rectangle = (x, y, w, h)
                break

        # If a car is found in the blue rectangle, update the most recently added car
        if car_in_blue_rectangle:
            most_recent_car = car_data.get_most_recent_car()
            print(f"Most recent car: {most_recent_car}")  # Debug print
            if most_recent_car and b'registration_number' in most_recent_car:
                registration_number = most_recent_car[b'registration_number'].decode()
                x, y, w, h = car_in_blue_rectangle
                car_data.set_car_info(registration_number, 'moving', x, y, x + w, y + h)
            else:
                print("Error: No most recent car found or registration_number key missing")


        # Draw two vertical lines for entry and exit gates with dynamic colors
        entry_gate_color = (0, 255, 0) if parking_gate_data.gate_status[0] == 'open' else (0, 0, 255)
        exit_gate_color = (0, 255, 0) if parking_gate_data.gate_status[1] == 'open' else (0, 0, 255)

        entry_gate_x = int(width * 2.6 / 4)
        entry_gate_y_start = int(height * 0.7 / 4)
        entry_gate_y_end = int(height * 1.7 / 4)


        exit_gate_x = int(width * 2.6 / 4)
        exit_gate_y_start = int(height * 2 / 4)
        exit_gate_y_end = int(height * 3 / 4)

        cv2.line(frame, (entry_gate_x, entry_gate_y_start), (entry_gate_x, entry_gate_y_end), entry_gate_color, 10)
        cv2.line(frame, (exit_gate_x, exit_gate_y_start), (exit_gate_x, exit_gate_y_end), exit_gate_color, 10)

        # Display all debugging windows
        cv2.imshow('Original', frame)

        if frame_count % 100 == 0:
            car_data.display_all_cars()

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release everything
    cap.release()
    cv2.destroyAllWindows()

# Use the script
if __name__ == "__main__":
    process_video(VIDEO_PATH, SKIP_FRAMES)