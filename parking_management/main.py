import threading
import os
import sys

# Add the parent directory to the sys.path so that the modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from redis_db.car_data import CarData
from video_processing_parking.app import process_video as process_parking_video, VIDEO_PATH as PARKING_VIDEO_PATH, SKIP_FRAMES as PARKING_SKIP_FRAMES
# from video_processing_gate.app import process_video as process_gate_video, VIDEO_PATH as GATE_VIDEO_PATH, SKIP_FRAMES as GATE_SKIP_FRAMES
# from backend.app import app

def run_parking_video_processing():
    process_parking_video(PARKING_VIDEO_PATH, PARKING_SKIP_FRAMES)

# def run_gate_video_processing():
#     process_gate_video(GATE_VIDEO_PATH, GATE_SKIP_FRAMES)

# def run_backend_server():
#     app.run(debug=True, use_reloader=False)  # use_reloader=False to prevent the server from running twice

if __name__ == "__main__":
    car_data = CarData()

    # Remove all cars from the database
    car_data.remove_all_cars()
    
    # Create threads for video processing and backend server
    video_parking_thread = threading.Thread(target=run_parking_video_processing)

    # video_gate_thread = threading.Thread(target=run_gate_video_processing)
    # backend_thread = threading.Thread(target=run_backend_server)

    # Start the threads
    video_parking_thread.start()

    # video_gate_thread.start()
    # backend_thread.start()

    # Wait for both threads to complete
    video_parking_thread.join()

    # video_gate_thread.join()
    # backend_thread.join()