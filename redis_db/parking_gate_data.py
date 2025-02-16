from .redis_client import RedisClient

class ParkingGateData(RedisClient):
    def __init__(self):
        super().__init__()
        self.gate_status = {
            0: 'closed',  # Entry gate
            1: 'closed'   # Exit gate
        }

    def set_gate_status(self, gate_id, status):
        key = f"gate:{gate_id}" # 0 - entry gate, 1 - exit gate
        self.hset(key, 'status', status) # open, closed
        self.gate_status[gate_id] = status

    def get_gate_status(self, gate_id):
        key = f"gate:{gate_id}"
        return self.hget(key, 'status')

    def update_gate_status(self, gate_id, new_status):
        key = f"gate:{gate_id}"
        self.hset(key, 'status', new_status)

    def delete_gate_status(self, gate_id):
        key = f"gate:{gate_id}"
        self.hdel(key, 'status')

    def get_all_gates(self):
        keys = self.keys('gate:*')
        gates = []
        for key in keys:
            gate_info = self.hgetall(key)
            gate_info['gate_id'] = key.decode().split(':')[1]
            gates.append(gate_info)
        return gates