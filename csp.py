# csp.py

from typing import List, Dict, Tuple
from data_models import Drone, DeliveryPoint, NoFlyZone
from astar import intersects_nofly

def is_assignment_valid(drone: Drone, delivery: DeliveryPoint, noflyzones: List[NoFlyZone]) -> bool:
    if delivery.weight > drone.max_weight:
        return False
    if intersects_nofly(drone.start_pos, delivery.pos, noflyzones):
        return False
    # Batarya kontrolü (örnek): 1 birim mesafe = 1 birim enerji tüketimi
    distance = ((drone.start_pos[0] - delivery.pos[0])**2 + (drone.start_pos[1] - delivery.pos[1])**2) ** 0.5
    if distance > drone.battery:
        return False
    return True

def assign_deliveries(drones: List[Drone], deliveries: List[DeliveryPoint], noflyzones: List[NoFlyZone]) -> Dict[int, List[int]]:
    assignments: Dict[int, List[int]] = {drone.id: [] for drone in drones}
    assigned_deliveries = set()

    for delivery in sorted(deliveries, key=lambda x: -x.priority):  # Öncelikli teslimatları önce atar
        for drone in drones:
            if is_assignment_valid(drone, delivery, noflyzones):
                assignments[drone.id].append(delivery.id)
                assigned_deliveries.add(delivery.id)
                break

    return assignments
