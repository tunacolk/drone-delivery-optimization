# test_and_visualize.py

import matplotlib.pyplot as plt
from data_generator import generate_random_drones, generate_random_deliveries, generate_random_nofly_zones
from genetic_algorithm import run_ga

def run_scenario(drone_count, delivery_count, nfz_count):
    drones = generate_random_drones(drone_count)
    deliveries = generate_random_deliveries(delivery_count)
    noflyzones = generate_random_nofly_zones(nfz_count)
    
    solution = run_ga(drones, deliveries, noflyzones)
    print("En iyi birey dağılımı:")
    for drone_id, tasks in solution.items():
        print(f"Drone {drone_id} -> {len(tasks)} teslimat: {tasks}")

    # Performans metrikleri

    total_deliveries = sum(len(v) for v in solution.values())
    total_energy = 0
    for drone in drones:
        pos = drone.start_pos
        for delivery_id in solution[drone.id]:
            delivery = next(d for d in deliveries if d.id == delivery_id)
            dist = ((pos[0]-delivery.pos[0])**2 + (pos[1]-delivery.pos[1])**2)**0.5
            total_energy += dist
            pos = delivery.pos

    print(f"Drone: {drone_count}, Teslimat: {delivery_count}, No-Fly Zones: {nfz_count}")
    print(f"Tamamlanan teslimat sayısı: {total_deliveries}")
    print(f"Ortalama enerji tüketimi: {total_energy / drone_count:.2f}")
    
    total_deliveries = sum(len(v) for v in solution.values())
    unique_deliveries = len(set(did for v in solution.values() for did in v))

    print(f"Toplam teslimat sayısı (tekrar dahil): {total_deliveries}")
    print(f"Benzersiz teslimat sayısı: {unique_deliveries}")

    
    return drones, deliveries, noflyzones, solution

def plot_solution(drones, deliveries, noflyzones, solution):
    plt.figure(figsize=(10, 10))
    
    # Teslimat noktaları
    for d in deliveries:
        plt.plot(d.pos[0], d.pos[1], 'bo')
        plt.text(d.pos[0]+1, d.pos[1]+1, f"{d.id}", fontsize=8)

    # Dronelar ve yolları
        # Dronelar ve yolları (her teslimat için ayrı çizgi)
    colors = ['r', 'g', 'b', 'm', 'c', 'y']  # Farklı drone'lar için renkler
    for idx, drone in enumerate(drones):
        color = colors[idx % len(colors)]
        start_pos = drone.start_pos
        plt.scatter(start_pos[0], start_pos[1], marker='s', color='black')
        plt.text(start_pos[0], start_pos[1]+1, f"Drone {drone.id}", fontsize=9)

        for did in solution[drone.id]:
            delivery = next(d for d in deliveries if d.id == did)
            end_pos = delivery.pos
            plt.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], linestyle='--', color=color, label=f'Drone {drone.id}' if did == solution[drone.id][0] else "")


    # No-fly zones
    for nfz in noflyzones:
        coords = nfz.coordinates + [nfz.coordinates[0]]
        xs, ys = zip(*coords)
        plt.fill(xs, ys, color='red', alpha=0.3)
        plt.text(coords[0][0], coords[0][1], f"NFZ {nfz.id}", fontsize=8, color='red')

    plt.legend()
    plt.title("Drone Teslimat Rotaları")
    plt.grid(True)
    plt.show()

# Senaryo örneği:
if __name__ == "__main__":
    drones, deliveries, noflyzones, solution = run_scenario(4, 25,5)#aryo 1
    plot_solution(drones, deliveries, noflyzones, solution)
    for drone in drones:
        assigned = solution.get(drone.id, [])
        print(f"Drone {drone.id} -> {len(assigned)} teslimat")
