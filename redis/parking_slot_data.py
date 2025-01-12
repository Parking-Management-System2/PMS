from redis_client import RedisClient


class ParkingSlotData(RedisClient):
    def __init__(self):
        super().__init__()

    @classmethod
    def set_parking_slot_info(cls, slot_id, position_upper_x, position_upper_y, position_bottom_x, position_bottom_y,
                              status, current_car_registration=None):
        key = f"parking_slot:{slot_id}"
        cls().hset(key, "position_upper_x", position_upper_x)
        cls().hset(key, "position_upper_y", position_upper_y)
        cls().hset(key, "position_bottom_x", position_bottom_x)
        cls().hset(key, "position_bottom_y", position_bottom_y)
        cls().hset(key, "status", status)
        if current_car_registration:
            cls().hset(key, "current_car_registration", current_car_registration)

    @classmethod
    def get_parking_slot_info(cls, slot_id):
        key = f"parking_slot:{slot_id}"
        return cls().hgetall(key)

    @classmethod
    def get_all_parking_slots(cls):
        keys = cls().client.keys("parking_slot:*")
        return [key.decode().split(":")[1] for key in keys]

    @classmethod
    def update_parking_slot_status(cls, slot_id, new_status):
        key = f"parking_slot:{slot_id}"
        cls().hset(key, "status", new_status)

    @classmethod
    def assign_car_to_slot(cls, slot_id, car_registration):
        key = f"parking_slot:{slot_id}"
        cls().hset(key, "current_car_registration", car_registration)
        cls().update_parking_slot_status(slot_id, "occupied")

    @classmethod
    def remove_car_from_slot(cls, slot_id):
        key = f"parking_slot:{slot_id}"
        parking_slot = cls().get_parking_slot_info(slot_id)
        if parking_slot.get('reserved_car_registration'):
            cls().update_parking_slot_status(slot_id, "reserved")
        else:
            cls().update_parking_slot_status(slot_id, "available")
        cls().hset(key, "current_car_registration", "")
