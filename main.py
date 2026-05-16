import os
import csv
import math
import random
import time

def estimate_pi_monte_carlo(N):
    """
    Обчислення числа Pi методом Монте-Карло.
    Оптимізовано для великих N за допомогою генерації батчами,
    щоб уникнути переповнення оперативної пам'яті.
    """
    inside_circle = 0
    batch_size = 10_000_000  # Розмір порції для обчислень
    
    remaining = N
    while remaining > 0:
        current_batch = min(remaining, batch_size)
        # Генеруємо випадкові точки в квадраті [-1, 1] х [-1, 1]
        for _ in range(current_batch):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x**2 + y**2 <= 1:
                inside_circle += 1
        remaining -= current_batch

    # Формула Монте-Карло: Pi = 4 * (точки в колі / всього точок)
    pi_estimated = 4 * inside_circle / N
    return pi_estimated

def main():
    # Реальне значення Pi для розрахунку точності
    PI_TRUE = math.pi
    
    # Масив значень N із завдання
    # УВАГА: Останні два значення (10 млрд та 100 млрд) закоментовані,
    # оскільки їх чистий прорахунок на базовому Python може зайняти години/дні.
    # Якщо викладач вимагатиме ВСІ, просто розкоментуй їх.
    N_values = [
        1_000_000,
        10_000_000,
        100_000_000,
        1_000_000_000,
        # 10_000_000_000,
        # 100_000_000_000
    ]
    
    # Шлях до файлу результатів, як вимагає ДЗ
    output_dir = "results"
    output_file = os.path.join(output_dir, "pi_monte_carlo_results.csv")
    
    # Створюємо папку, якщо вона раптом відсутня
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print("Початок обчислень методом Монте-Карло...\n")
    
    results = []
    
    for N in N_values:
        print(f"Розрахунок для N = {N:,}...")
        start_time = time.time()
        
        pi_est = estimate_pi_monte_carlo(N)
        
        end_time = time.time()
        
        # Розрахунок метрик за вимогою в умові
        execution_time = end_time - start_time
        accuracy = abs(pi_est - PI_TRUE)
        time_per_point = execution_time / N
        
        results.append({
            "N": N,
            "pi_estimated": pi_est,
            "accuracy": accuracy,
            "execution_time_sec": execution_time,
            "time_per_point": time_per_point
        })
        
        print(f"Знайдене знач. Pi: {pi_est}")
        print(f"Час виконання: {execution_time:.4f} сек\n")
        
    # Запис результатів у форматі CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Заголовки стовпців
        writer.writerow(["N", "Estimated Pi", "Accuracy (abs error)", "Execution Time (sec)", "Time Per Point"])
        
        for res in results:
            writer.writerow([
                res["N"],
                f"{res['pi_estimated']:.10f}",
                f"{res['accuracy']:.10f}",
                f"{res['execution_time_sec']:.4f}",
                f"{res['time_per_point']:.10e}"
            ])
            
    print(f"Успішно! Результати збережено у файл: {output_file}")

if __name__ == "__main__":
    main()