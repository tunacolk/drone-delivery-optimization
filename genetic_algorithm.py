#ga
import random
from typing import List, Dict
from data_models import Drone, DeliveryPoint, NoFlyZone
from csp import is_assignment_valid
from astar import intersects_nofly


def generate_initial_population(
    drones: List[Drone],
    deliveries: List[DeliveryPoint],
    noflyzones: List[NoFlyZone],
    size: int = 10
) -> List[Dict[int, List[int]]]:
    """İlk popülasyonu üretir."""
    population = []
    for _ in range(size):
        individual = {drone.id: [] for drone in drones}
        shuffled = deliveries[:]
        random.shuffle(shuffled)
        assigned_deliveries = set()

        for delivery in shuffled:
            if delivery.id in assigned_deliveries:
                continue
            random.shuffle(drones)
            for drone in drones:
                if is_assignment_valid(drone, delivery, noflyzones):
                    individual[drone.id].append(delivery.id)
                    assigned_deliveries.add(delivery.id)
                    break
        population.append(individual)
    return population


def fitness(
    individual: Dict[int, List[int]],
    drones: List[Drone],
    deliveries: List[DeliveryPoint],
    noflyzones: List[NoFlyZone]
) -> float:
    """Bir bireyin uygunluğunu hesaplar."""
    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}

    total_energy = 0
    delivery_count = 0
    violations = 0

    for drone_id, assigned_ids in individual.items():
        drone = drone_map[drone_id]
        pos = drone.start_pos
        battery = drone.battery

        for did in assigned_ids:
            delivery = delivery_map[did]
            dx, dy = pos[0] - delivery.pos[0], pos[1] - delivery.pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            energy = distance  # Basit enerji modeli

            if delivery.weight > drone.max_weight or energy > battery:
                violations += 1
                continue

            if intersects_nofly(pos, delivery.pos, noflyzones):
                violations += 1
                continue

            total_energy += energy
            battery -= energy
            pos = delivery.pos
            delivery_count += 1

    return delivery_count * 50 - total_energy * 0.1 - violations * 1000


def crossover(parent1: Dict[int, List[int]], parent2: Dict[int, List[int]]) -> Dict[int, List[int]]:
    """İki ebeveynden geçerli bir çocuk birey üretir."""
    child = {drone_id: [] for drone_id in parent1}
    assigned = set()

    for drone_id in parent1:
        deliveries = parent1[drone_id] if random.random() < 0.5 else parent2[drone_id]
        for did in deliveries:
            if did not in assigned:
                child[drone_id].append(did)
                assigned.add(did)

    return child


def mutate(individual: Dict[int, List[int]], deliveries: List[DeliveryPoint]) -> None:
    """Birey üzerinde rastgele mutasyon uygular."""
    drone_ids = list(individual.keys())
    if len(drone_ids) < 2:
        return

    d1, d2 = random.sample(drone_ids, 2)
    if not individual[d1] or not individual[d2]:
        return

    i1 = random.randint(0, len(individual[d1]) - 1)
    i2 = random.randint(0, len(individual[d2]) - 1)

    did1 = individual[d1][i1]
    did2 = individual[d2][i2]

    if did1 == did2:
        return

    individual[d1][i1], individual[d2][i2] = did2, did1


def run_ga(
    drones: List[Drone],
    deliveries: List[DeliveryPoint],
    noflyzones: List[NoFlyZone],
    generations: int = 20,
    pop_size: int = 10
) -> Dict[int, List[int]]:
    """Genetik algoritmayı çalıştırır."""
    population = generate_initial_population(drones, deliveries, noflyzones, size=pop_size)

    for _ in range(generations):
        population.sort(
            key=lambda ind: fitness(ind, drones, deliveries, noflyzones),
            reverse=True
        )
        new_population = population[:2]  # Elitizm: En iyi 2 birey doğrudan alınır

        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:5], 2)
            child = crossover(parent1, parent2)
            if random.random() < 0.2:
                mutate(child, deliveries)
            new_population.append(child)

        population = new_population

    best = max(population, key=lambda ind: fitness(ind, drones, deliveries, noflyzones))
    return best
