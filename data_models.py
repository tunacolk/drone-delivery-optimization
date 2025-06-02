# data_models.py

from typing import Tuple, List

class Drone:
    def __init__(self, drone_id: int, max_weight: float, battery: int, speed: float, start_pos: Tuple[float, float]):
        self.id = drone_id
        self.max_weight = max_weight
        self.battery = battery  # in mAh
        self.speed = speed  # in m/s
        self.start_pos = start_pos
        self.current_pos = start_pos
        self.available = True
        self.current_battery = battery

    def __repr__(self):
        return f"<Drone {self.id} | Battery: {self.battery} | MaxWeight: {self.max_weight}kg>"

class DeliveryPoint:
    def __init__(self, delivery_id: int, pos: Tuple[float, float], weight: float, priority: int, time_window: Tuple[str, str]):
        self.id = delivery_id
        self.pos = pos
        self.weight = weight
        self.priority = priority  # 1 (low) to 5 (high)
        self.time_window = time_window  # ("09:00", "10:00")

    def __repr__(self):
        return f"<Delivery {self.id} | Weight: {self.weight}kg | Priority: {self.priority}>"

class NoFlyZone:
    def __init__(self, zone_id: int, coordinates: List[Tuple[float, float]], active_time: Tuple[str, str]):
        self.id = zone_id
        self.coordinates = coordinates  # List of (x, y) tuples defining polygon
        self.active_time = active_time  # ("09:30", "11:00")

    def __repr__(self):
        return f"<NoFlyZone {self.id} | Active: {self.active_time}>"
