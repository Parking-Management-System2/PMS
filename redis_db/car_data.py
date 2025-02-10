from .redis_client import RedisClient
from .parking_slot_data import ParkingSlotData
from .validation_result import ValidationResult

class CarData(RedisClient):
    def __init__(self):
        super().__init__()
        self.car_last_seen = {}

    def set_car_info(self, registration_number, status, position_upper_x, position_upper_y, position_bottom_x, position_bottom_y):
        key = f"car:{registration_number}"
        self.hset(key, 'status', status)
        self.hset(key, 'position_upper_x', position_upper_x)
        self.hset(key, 'position_upper_y', position_upper_y)
        self.hset(key, 'position_bottom_x', position_bottom_x)
        self.hset(key, 'position_bottom_y', position_bottom_y)

    def get_car_info(self, registration_number):
        key = f"car:{registration_number}"
        return self.hgetall(key)

    def update_car_status(self, registration_number, new_status):
        key = f"car:{registration_number}"
        self.hset(key, "status", new_status)

    def update_car_position(self, registration_number, position_upper_x, position_upper_y, position_bottom_x, position_bottom_y):
        key = f"car:{registration_number}"
        self.hset(key, 'position_upper_x', position_upper_x)
        self.hset(key, 'position_upper_y', position_upper_y)
        self.hset(key, 'position_bottom_x', position_bottom_x)
        self.hset(key, 'position_bottom_y', position_bottom_y)

    def remove_car(self, registration_number):
        key = f"car:{registration_number}"
        self.delete(key)

    def display_all_cars(self):
        keys = self.keys('car:*')
        for key in keys:
            print(self.hgetall(key))

    def update_cars(self, cars, frame_count, max_undetected_frames):
        detected_cars = set()
        for (x, y, w, h) in cars:
            registration_number = f"{x}_{y}_{w}_{h}"
            self.set_car_info(registration_number, 'detected', x, y, x + w, y + h)
            self.car_last_seen[registration_number] = frame_count
            detected_cars.add(registration_number)

        # Remove cars that have not been detected for more than max_undetected_frames
        for registration_number in list(self.car_last_seen.keys()):
            if registration_number not in detected_cars and frame_count - self.car_last_seen[registration_number] > max_undetected_frames:
                self.remove_car(registration_number)
                del self.car_last_seen[registration_number]