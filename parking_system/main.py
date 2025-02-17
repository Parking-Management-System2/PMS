import os
import sys
import threading

# Add the parent directory to the sys.path so that the modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.car_data import CarData
from redis_db.parking_gate_data import ParkingGateData
from data_display.live_display import start_live_display  # New import

from video_processing_parking.app import process_video as process_parking_video, VIDEO_PATH as PARKING_VIDEO_PATH, \
    SKIP_FRAMES as PARKING_SKIP_FRAMES
from video_processing_gate.app import LicensePlateRecognizer, VIDEO_PATH as GATE_VIDEO_PATH

def run_parking_video_processing(car_data, parking_gate_data):
    process_parking_video(PARKING_VIDEO_PATH, PARKING_SKIP_FRAMES, car_data, parking_gate_data)

def run_gate_video_processing(car_data, parking_gate_data):
    recognizer = LicensePlateRecognizer(car_data, parking_gate_data, gate_open_duration=20)
    recognizer.process_video(GATE_VIDEO_PATH)

if __name__ == "__main__":
    car_data = CarData()
    parking_gate_data = ParkingGateData()
    # Remove all cars from the database
    car_data.remove_all_cars()

    # Initialize gate statuses
    parking_gate_data.set_gate_status(0, 'closed')  # Entry gate closed
    parking_gate_data.set_gate_status(1, 'closed')  # Exit gate open

    # Create threads for video processing
    video_parking_thread = threading.Thread(
        target=run_parking_video_processing,
        args=(car_data, parking_gate_data),
        daemon=True
    )
    video_gate_thread = threading.Thread(
        target=run_gate_video_processing,
        args=(car_data, parking_gate_data),
        daemon=True
    )

    # Start the threads
    video_parking_thread.start()
    video_gate_thread.start()

    # Start the live display GUI in the main thread
    start_live_display(car_data, parking_gate_data)

    # No need to join threads since they're daemon threads
    # The program will exit when the GUI window is closed