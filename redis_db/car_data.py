import uuid
from .redis_client import RedisClient

class CarData(RedisClient):
    def __init__(self):
        super().__init__()
        self.car_last_seen = {}

    def set_car_info(self, registration_number, status, position_upper_x, position_upper_y, position_bottom_x,
                     position_bottom_y):
        key = f"car:{registration_number}"
        self.hset(key, 'registration_number', registration_number)
        self.hset(key, 'status', status)
        self.hset(key, 'position_upper_x', position_upper_x)
        self.hset(key, 'position_upper_y', position_upper_y)
        self.hset(key, 'position_bottom_x', position_bottom_x)
        self.hset(key, 'position_bottom_y', position_bottom_y)
        # Add the key to the ordered list if it doesn't already exist
        if not self.client.sismember('car_keys_set', key):
            self.client.rpush('car_keys', key)
            self.client.sadd('car_keys_set', key)

    def get_car_info(self, registration_number):
        key = f"car:{registration_number}"
        return self.hgetall(key)

    def update_car_status(self, registration_number, new_status):
        key = f"car:{registration_number}"
        self.hset(key, "status", new_status)

    def update_car_position(self, registration_number, position_upper_x, position_upper_y, position_bottom_x,
                            position_bottom_y):
        key = f"car:{registration_number}"
        self.hset(key, 'position_upper_x', position_upper_x)
        self.hset(key, 'position_upper_y', position_upper_y)
        self.hset(key, 'position_bottom_x', position_bottom_x)
        self.hset(key, 'position_bottom_y', position_bottom_y)

    def remove_car(self, registration_number):
        key = f"car:{registration_number}"
        self.delete(key)
        # Remove the key from the ordered list and set
        self.client.lrem('car_keys', 0, key)
        self.client.srem('car_keys_set', key)

    def remove_all_cars(self):
        keys = self.keys('car:*')
        for key in keys:
            self.delete(key)
        # Clear the ordered list and set
        self.client.delete('car_keys')
        self.client.delete('car_keys_set')    

    def display_all_cars(self):
        keys = self.keys('car:*')
        for key in keys:
            print(f'{key} : {self.hgetall(key)}')

    def get_all_cars(self):
        keys = self.keys('car:*')
        cars = []
        for key in keys:
            car_info = self.hgetall(key)
            car_info['registration_number'] = key.decode().split(':')[1]
            cars.append(car_info)
        return cars

    def get_most_recent_car(self):
        # Get the last element from the ordered list
        most_recent_key = self.client.lindex('car_keys', -1)
        if most_recent_key:
            registration_number = most_recent_key.decode().split(':')[1]
            car_info = self.get_car_info(registration_number)
            return car_info
        return None

    def get_nearest_car(self, x, y, max_distance=150):
        """Finds the nearest stored car within max_distance."""
        keys = self.keys('car:*')
        closest_car = None
        min_distance = max_distance

        for key in keys:
            car_info = self.hgetall(key)
            if not car_info:
                continue

            try:
                car_x = int(car_info.get(b'position_upper_x', b'0').decode())
                car_y = int(car_info.get(b'position_upper_y', b'0').decode())
                distance = ((car_x - x) ** 2 + (car_y - y) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_car = key
            except (KeyError, ValueError):
                continue

        return closest_car

    def update_cars(self, cars, frame_count):
        detected_cars = set()

        for (x, y, w, h) in cars:
            existing_car_key = self.get_nearest_car(x, y)

            if existing_car_key:
                # Update existing car's position
                self.hset(existing_car_key, 'position_upper_x', x)
                self.hset(existing_car_key, 'position_upper_y', y)
                self.hset(existing_car_key, 'position_bottom_x', x + w)
                self.hset(existing_car_key, 'position_bottom_y', y + h)
                registration_number = existing_car_key.decode().split(':')[1]

                self.car_last_seen[registration_number] = frame_count
                detected_cars.add(registration_number)