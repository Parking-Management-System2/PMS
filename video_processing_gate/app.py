import os
import cv2
import easyocr
import re
import concurrent.futures
import threading
import time
from redis_db.car_data import CarData
from redis_db.parking_gate_data import ParkingGateData

VIDEO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '2', 'GATE4.mp4'))

# Initialize EasyOCR (English) with GPU if available
reader = easyocr.Reader(['en'], gpu=False)

# Registration pattern that meets the conditions
registration_pattern = re.compile(r'^[A-Z]{2,3} [A-Z0-9]{4,5}$')

class LicensePlateRecognizer:
    def __init__(self, car_data, parking_gate_data, gate_open_duration=15):
        self.recognized_plates = []
        self.lock = threading.Lock()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.futures = []
        self.car_data = car_data
        self.parking_gate_data = parking_gate_data
        self.gate_open_duration = gate_open_duration

        # Move 100 pixels right and 150 pixels up
        self.roi = {
            'x': 0,  # New X: 500
            'y': 100,  # New Y: 350
            'width': 1280,
            'height': 350
        }

    def preprocess_frame(self, frame):
        """Preprocess frame for better OCR results"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply adaptive thresholding
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 2)

    def process_frame_ocr(self, frame):
        """Process frame for license plate recognition"""
        try:
            # Preprocess the frame
            processed = self.preprocess_frame(frame)

            # Perform OCR
            results = reader.readtext(processed, detail=0, paragraph=True)
            text = " ".join(results).strip().upper()

            # Validate against registration pattern
            if registration_pattern.match(text):
                return text
        except Exception as e:
            print(f"OCR processing error: {str(e)}")
        return None

    def update_recognized_plates(self, text):
        """Thread-safe update of recognized plates list"""
        with self.lock:
            if text and text not in self.recognized_plates:
                self.recognized_plates.append(text)
                print(f"New plate recognized: {text}")
                self.car_data.set_car_info(text, 'detected', 0, 0, 0, 0)
                self.open_gate_temporarily()

    def open_gate_temporarily(self):
        """Open the entry gate for a specified duration and then close it"""
        self.parking_gate_data.set_gate_status(0, 'open')
        threading.Timer(self.gate_open_duration, self.close_gate).start()

    def close_gate(self):
        """Close the entry gate"""
        self.parking_gate_data.set_gate_status(0, 'closed')

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return

        frame_count = 0
        frames = [750, 2800, 4000, 5375, 7375, 8925, 11600]
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Resize frame for display
            frame = cv2.resize(frame, (1280, 720))
            frame_count += 1

            cv2.putText(frame, f"Frame: {frame_count}", (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 5)

            # Process specific frames for performance balance
            if frame_count in frames:
                # Extract ROI for license plate
                roi = frame[self.roi['y']:self.roi['y'] + self.roi['height'],
                            self.roi['x']:self.roi['x'] + self.roi['width']]

                # Submit OCR task to thread pool
                future = self.executor.submit(self.process_frame_ocr, roi)
                future.add_done_callback(
                    lambda f: self.update_recognized_plates(f.result()))

            # Draw ROI rectangle
            cv2.rectangle(frame,
                          (self.roi['x'], self.roi['y']),
                          (self.roi['x'] + self.roi['width'], self.roi['y'] + self.roi['height']),
                          (0, 255, 0), 2)

            # Display recognized plates in top-right corner
            with self.lock:
                for i, plate in enumerate(self.recognized_plates):
                    text_size = cv2.getTextSize(plate, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
                    x = frame.shape[1] - text_size[0] - 20  # Right-aligned
                    y = 40 + i * 40
                    cv2.putText(frame, plate, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow('License Plate Recognition', frame)

            time.sleep(0.006)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        self.executor.shutdown(wait=False)
        cap.release()
        cv2.destroyAllWindows()
        print(f"Final recognized plates: {self.recognized_plates}")

if __name__ == "__main__":
    car_data = CarData()
    parking_gate_data = ParkingGateData()
    recognizer = LicensePlateRecognizer(car_data, parking_gate_data, gate_open_duration=10)
    recognizer.process_video(VIDEO_PATH)