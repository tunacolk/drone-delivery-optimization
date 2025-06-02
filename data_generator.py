    # data_generator.py

import random
from typing import List, Tuple
from data_models import Drone, DeliveryPoint, NoFlyZone

def generate_random_drones(n: int) -> List[Drone]:
        drones = []
        for i in range(n):
            max_weight = round(random.uniform(2.0, 10.0), 2)  # kg
            battery = random.randint(1000, 5000)              # mAh
            speed = round(random.uniform(5.0, 15.0), 2)       # m/s
            start_pos = (random.uniform(0, 100), random.uniform(0, 100))  # x,y in meters
            drones.append(Drone(i, max_weight, battery, speed, start_pos))
        return drones

def generate_random_deliveries(n: int) -> List[DeliveryPoint]:
        deliveries = []
        for i in range(n):
            pos = (random.uniform(0, 100), random.uniform(0, 100))  # x,y in meters
            weight = round(random.uniform(0.5, 5.0), 2)              # kg
            priority = random.randint(1, 5)
            hour = random.randint(9, 17)
            time_window = (f"{hour:02d}:00", f"{hour+1:02d}:00")
            deliveries.append(DeliveryPoint(i, pos, weight, priority, time_window))
        return deliveries

def generate_random_nofly_zones(n: int) -> List[NoFlyZone]:
        zones = []
        for i in range(n):
            # Basit bir dörtgen oluştur
            x = random.uniform(10, 90)
            y = random.uniform(10, 90)
            size = random.uniform(5, 15)
            coordinates = [
                (x, y),
                (x + size, y),
                (x + size, y + size),
                (x, y + size)
            ]
            start_hour = random.randint(9, 16)
            active_time = (f"{start_hour:02d}:00", f"{start_hour + 1:02d}:00")
            zones.append(NoFlyZone(i, coordinates, active_time))
        return zones
