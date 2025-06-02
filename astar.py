#a*
import heapq
import math
from typing import List, Tuple
from shapely.geometry import LineString, Polygon
from data_models import DeliveryPoint, NoFlyZone, Drone


def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def intersects_nofly(p1: Tuple[float, float], p2: Tuple[float, float], noflyzones: List[NoFlyZone]) -> bool:
    path = LineString([p1, p2])
    for zone in noflyzones:
        polygon = Polygon(zone.coordinates)
        if path.intersects(polygon):
            return True
    return False


def calculate_cost(drone: Drone, p1: Tuple[float, float], p2: Tuple[float, float], weight: float, priority: int) -> float:
    distance = euclidean_distance(p1, p2)
    return (distance * weight) + (priority * 100)


def heuristic(current: Tuple[float, float], goal: Tuple[float, float], noflyzones: List[NoFlyZone]) -> float:
    penalty = 500 if intersects_nofly(current, goal, noflyzones) else 0
    return euclidean_distance(current, goal) + penalty


def reroute_around_nofly(p1: Tuple[float, float], p2: Tuple[float, float], noflyzones: List[NoFlyZone]) -> List[Tuple[float, float]]:
    for zone in noflyzones:
        polygon = Polygon(zone.coordinates)
        if LineString([p1, p2]).intersects(polygon):
            corners = list(polygon.exterior.coords)[:-1]  # polygon köşeleri
            reroutes = []
            for c1 in corners:
                for c2 in corners:
                    if c1 == c2:
                        continue
                    if not intersects_nofly(p1, c1, noflyzones) and \
                       not intersects_nofly(c1, c2, noflyzones) and \
                       not intersects_nofly(c2, p2, noflyzones):
                        reroutes.append([p1, c1, c2, p2])
            if reroutes:
                return min(reroutes, key=lambda route: sum(euclidean_distance(route[i], route[i+1]) for i in range(len(route)-1)))
    return [p1, p2]


def a_star(drone: Drone, deliveries: List[DeliveryPoint], noflyzones: List[NoFlyZone]) -> List[int]:
    open_set = []
    heapq.heappush(open_set, (0, drone.start_pos, [], 0.0))  # (priority, current_pos, visited_ids, cost_so_far)

    best_path = []
    best_cost = float("inf")

    while open_set:
        _, current_pos, visited, cost_so_far = heapq.heappop(open_set)

        if len(visited) == len(deliveries):
            if cost_so_far < best_cost:
                best_cost = cost_so_far
                best_path = visited
            continue

        for delivery in deliveries:
            if delivery.id in visited:
                continue
            if delivery.weight > drone.max_weight:
                continue

            path = reroute_around_nofly(current_pos, delivery.pos, noflyzones)
            total_path_cost = 0
            for i in range(len(path) - 1):
                total_path_cost += calculate_cost(drone, path[i], path[i + 1], delivery.weight, delivery.priority)

            new_cost = cost_so_far + total_path_cost
            est_total = new_cost + heuristic(path[-1], delivery.pos, noflyzones)
            heapq.heappush(open_set, (est_total, path[-1], visited + [delivery.id], new_cost))

    return best_path
