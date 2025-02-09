from .redis_client import RedisClient
from .parking_slot_data import ParkingSlotData
from .validation_result import ValidationResult

class CarData(RedisClient):
    def __init__(self):
        super().__init__()

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
        self.hdel(self, key)

    def display_all_cars(self):
        keys = self.keys('car:*')
        for key in keys:
            car_info = self.hgetall(key)
            print(f"Car {key}:")
            for field, value in car_info.items():
                print(f"  {field}: {value}")

    def update_cars(self, cars):
        for car in cars:
            x, y, w, h = car
            registration_number = f"car_{x}_{y}"
            self.set_car_info(registration_number, 'detected', x, y, x + w, y + h)

    def validate_car_entry(self, registration_number):
        car_info = self.get_car_info(registration_number)
        if car_info:
            return ValidationResult(False, "Car already exists")

        reserved_slot = None
        slot_info = None
        for slot_id in ParkingSlotData.get_all_parking_slots():
            slot_info = ParkingSlotData.get_parking_slot_info(slot_id)
            if slot_info.get('reserved_car_registration') == registration_number:
                reserved_slot = slot_id
                break

        if reserved_slot:
            if slot_info.get('status') == 'reserved':
                self.set_car_info(registration_number, 'parked', 0, 0, 0, 0)  # Add car entry to Redis
                return ValidationResult(True, f"Reserved slot {reserved_slot} is available")
            else:
                # Check if there is any parking slot which has reserved_car_registration empty and status available
                for slot_id in ParkingSlotData.get_all_parking_slots():
                    slot_info = ParkingSlotData.get_parking_slot_info(slot_id)
                    if slot_info.get('status') == 'available' and not slot_info.get('reserved_car_registration'):
                        self.set_car_info(registration_number, 'parked', 0, 0, 0, 0)  # Add car entry to Redis
                        return ValidationResult(True, f"Free slot {slot_id} is available")
                return ValidationResult(False, f"Reserved slot {reserved_slot} is occupied")
        else:
            for slot_id in ParkingSlotData.get_all_parking_slots():
                slot_info = ParkingSlotData.get_parking_slot_info(slot_id)
                if slot_info.get('status') == 'available' and not slot_info.get('reserved_car_registration'):
                    self.set_car_info(registration_number, 'parked', 0, 0, 0, 0)  # Add car entry to Redis
                    return ValidationResult(True, f"Free slot {slot_id} is available")

            return ValidationResult(False, "No free slots available")