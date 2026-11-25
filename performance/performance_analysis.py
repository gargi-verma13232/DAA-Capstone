"""
performance/performance_analysis.py - Empirical Performance Testing & Charting.

Measures actual execution times using time.perf_counter() across small and
large datasets for all four algorithms and saves charts into results/runtime_charts/.
"""

import os
import random
import tempfile
import time

if "MPLCONFIGDIR" not in os.environ:
    default_mpl = os.path.join(os.path.expanduser("~"), "AppData", "Local", "matplotlib")
    if not os.access(os.path.dirname(default_mpl), os.W_OK):
        os.environ["MPLCONFIGDIR"] = os.path.join(tempfile.gettempdir(), "mplconfig")

import matplotlib.pyplot as plt

from algorithms.sorting import merge_sort_parcels
from algorithms.knapsack import knapsack_01
from algorithms.dijkstra import build_graph, dijkstra
from algorithms.tsp import nearest_neighbor_tsp


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS_DIR = os.path.join(BASE_DIR, "results", "runtime_charts")


def generate_parcels(count, seed=42):
    """Generate a deterministic synthetic list of `count` parcels."""
    rng = random.Random(seed)
    parcels = []
    for i in range(count):
        parcels.append({
            "id": f"P{i + 1}",
            "weight": rng.randint(1, 15),
            "priority": rng.randint(10, 100),
            "deadline": rng.randint(1, 24),
            "location": f"Loc-{i % max(5, count // 3)}",
        })
    return parcels


def generate_graph(num_vertices, extra_edges_per_node=3, seed=42):
    """Generate a connected undirected weighted graph with `num_vertices` nodes."""
    rng = random.Random(seed)
    locations = [f"Loc-{i}" for i in range(num_vertices)]
    roads = []

    for i in range(num_vertices - 1):
        roads.append((locations[i], locations[i + 1], rng.randint(1, 20)))

    if num_vertices > 2:
        for i in range(num_vertices):
            for _ in range(extra_edges_per_node):
                j = rng.randint(0, num_vertices - 1)
                if i != j:
                    roads.append((locations[i], locations[j], rng.randint(1, 20)))

    return locations, build_graph(locations, roads)


def measure_time_ms(func, *args, repeats=3):
    """Measure average execution time in milliseconds using time.perf_counter()."""
    total = 0.0
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        total += (end - start)
    return (total / repeats) * 1000.0


def benchmark_individual_algorithms():
    """Run small-to-large scaling benchmarks for each algorithm."""
    sort_sizes = [50, 200, 500, 1000, 2500, 5000]
    sort_times = [measure_time_ms(merge_sort_parcels, generate_parcels(n), repeats=3) for n in sort_sizes]

    knapsack_sizes = [10, 25, 50, 100, 200, 300]
    knapsack_caps = [n * 2 for n in knapsack_sizes]
    knapsack_times = [
        measure_time_ms(knapsack_01, generate_parcels(n), cap, repeats=2)
        for n, cap in zip(knapsack_sizes, knapsack_caps)
    ]

    dijkstra_sizes = [20, 50, 100, 250, 500, 1000]
    dijkstra_times = []
    for v in dijkstra_sizes:
        locs, graph = generate_graph(v)
        dijkstra_times.append(measure_time_ms(dijkstra, graph, locs[0], repeats=3))

    tsp_stops = [5, 10, 20, 30, 50, 75]
    tsp_times = []
    for k in tsp_stops:
        locs, graph = generate_graph(max(100, k * 2))
        tsp_times.append(measure_time_ms(nearest_neighbor_tsp, graph, locs[0], locs[1:k + 1], repeats=2))

    return {
        "sort": (sort_sizes, sort_times),
        "knapsack": (knapsack_sizes, knapsack_caps, knapsack_times),
        "dijkstra": (dijkstra_sizes, dijkstra_times),
        "tsp": (tsp_stops, tsp_times),
    }


def benchmark_common_comparison():
    """Compare all four algorithms across common input sizes N = [10, 25, 50, 75, 100]."""
    common_sizes = [10, 25, 50, 75, 100]
    results = {"sizes": common_sizes, "sort": [], "knapsack": [], "dijkstra": [], "tsp": []}

    for n in common_sizes:
        parcels = generate_parcels(n)
        locs, graph = generate_graph(n + 1)
        stops = locs[1:n + 1]

        results["sort"].append(measure_time_ms(merge_sort_parcels, parcels, repeats=3))
        results["knapsack"].append(measure_time_ms(knapsack_01, parcels, n * 2, repeats=2))
        results["dijkstra"].append(measure_time_ms(dijkstra, graph, locs[0], repeats=3))
        results["tsp"].append(measure_time_ms(nearest_neighbor_tsp, graph, locs[0], stops, repeats=2))

    return results


def generate_charts(individual_data, comparison_data, output_dir=CHARTS_DIR):
    """Generate and save Matplotlib runtime charts in results/runtime_charts/."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Mini-Courier Planner: Individual Algorithm Runtime Scaling", fontsize=14, fontweight="bold")

    s_sizes, s_times = individual_data["sort"]
    axes[0, 0].plot(s_sizes, s_times, marker="o", color="#1f77b4", linewidth=2)
    axes[0, 0].set_title("Merge Sort - O(n log n)")
    axes[0, 0].set_xlabel("Number of Parcels (n)")
    axes[0, 0].set_ylabel("Execution Time (ms)")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)

    k_sizes, _, k_times = individual_data["knapsack"]
    axes[0, 1].plot(k_sizes, k_times, marker="s", color="#d62728", linewidth=2)
    axes[0, 1].set_title("0/1 Knapsack DP - O(n * W), W = 2n")
    axes[0, 1].set_xlabel("Number of Parcels (n)")
    axes[0, 1].set_ylabel("Execution Time (ms)")
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)

    d_sizes, d_times = individual_data["dijkstra"]
    axes[1, 0].plot(d_sizes, d_times, marker="^", color="#2ca02c", linewidth=2)
    axes[1, 0].set_title("Dijkstra's Algorithm - O((V + E) log V)")
    axes[1, 0].set_xlabel("Number of Locations (V)")
    axes[1, 0].set_ylabel("Execution Time (ms)")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)

    t_sizes, t_times = individual_data["tsp"]
    axes[1, 1].plot(t_sizes, t_times, marker="D", color="#9467bd", linewidth=2)
    axes[1, 1].set_title("Nearest Neighbor TSP (via Dijkstra) - O(k*(V+E)logV + k^2)")
    axes[1, 1].set_xlabel("Number of Delivery Stops (k)")
    axes[1, 1].set_ylabel("Execution Time (ms)")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    individual_path = os.path.join(output_dir, "runtime_individual.png")
    plt.savefig(individual_path, dpi=150)

    plt.figure(figsize=(9, 5.5))
    sizes = comparison_data["sizes"]
    plt.plot(sizes, comparison_data["sort"], marker="o", linewidth=2, label="Merge Sort O(n log n)")
    plt.plot(sizes, comparison_data["knapsack"], marker="s", linewidth=2, label="0/1 Knapsack DP O(n * W)")
    plt.plot(sizes, comparison_data["dijkstra"], marker="^", linewidth=2, label="Dijkstra O((V + E) log V)")
    plt.plot(sizes, comparison_data["tsp"], marker="D", linewidth=2, label="Nearest Neighbor TSP + Dijkstra")

    plt.title("Algorithm Runtime Comparison (Common Input Sizes)", fontsize=13, fontweight="bold")
    plt.xlabel("Input Size (N = Parcels / Vertices / Stops)")
    plt.ylabel("Execution Time (ms)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    comparison_path = os.path.join(output_dir, "runtime_comparison.png")
    plt.savefig(comparison_path, dpi=150)

    plt.show()
    plt.close("all")

    return individual_path, comparison_path


def print_performance_report(individual_data, comparison_data, chart_paths):
    """Print recorded execution times, theoretical complexities, and explanation."""
    print("\n============================================================")
    print("         PERFORMANCE ANALYSIS REPORT (ACTUAL TIMINGS)       ")
    print("============================================================")

    print("\n1. Individual Scaling Benchmarks (Small to Large Datasets):")

    print("\n  [A] Merge Sort (Parcel Prioritization)")
    print(f"  {'Input Size (n)':<18} {'Time (ms)':<12}")
    print("  " + "-" * 30)
    for n, t in zip(*individual_data["sort"]):
        print(f"  {n:<18} {t:<12.4f}")

    print("\n  [B] 0/1 Knapsack DP (Capacity W = 2 * n)")
    print(f"  {'Parcels (n)':<14} {'Capacity (W)':<14} {'Time (ms)':<12}")
    print("  " + "-" * 40)
    for n, cap, t in zip(*individual_data["knapsack"]):
        print(f"  {n:<14} {cap:<14} {t:<12.4f}")

    print("\n  [C] Dijkstra's Algorithm (E ~ 4V)")
    print(f"  {'Vertices (V)':<18} {'Time (ms)':<12}")
    print("  " + "-" * 30)
    for v, t in zip(*individual_data["dijkstra"]):
        print(f"  {v:<18} {t:<12.4f}")

    print("\n  [D] Nearest Neighbor TSP (with Dijkstra Shortest Paths)")
    print(f"  {'Delivery Stops (k)':<18} {'Time (ms)':<12}")
    print("  " + "-" * 30)
    for k, t in zip(*individual_data["tsp"]):
        print(f"  {k:<18} {t:<12.4f}")

    print("\n2. Side-by-Side Comparison (Common Input Size N):")
    header = f"  {'Size (N)':<10} {'Merge Sort':<14} {'Knapsack DP':<14} {'Dijkstra':<14} {'NN-TSP+Dijk':<14}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for i, n in enumerate(comparison_data["sizes"]):
        print(
            f"  {n:<10} "
            f"{comparison_data['sort'][i]:<14.4f} "
            f"{comparison_data['knapsack'][i]:<14.4f} "
            f"{comparison_data['dijkstra'][i]:<14.4f} "
            f"{comparison_data['tsp'][i]:<14.4f}"
        )

    print("\n3. Theoretical Time & Space Complexities:")
    print("  - Merge Sort          : Time = O(n log n),           Space = O(n)")
    print("  - 0/1 Knapsack DP     : Time = O(n * W),             Space = O(n * W)")
    print("  - Dijkstra's Alg.     : Time = O((V + E) log V),     Space = O(V + E)")
    print("  - Nearest Neighbor TSP: Time = O(k*(V+E)logV + k^2), Space = O(k^2 + V + E)")

    print("\n4. Observed Performance Explanation:")
    print("  - Merge Sort and single-source Dijkstra scale smoothly as O(n log n) and")
    print("    O((V + E) log V), staying fast even on large inputs.")
    print("  - 0/1 Knapsack DP depends on both parcel count n and capacity W. When W")
    print("    grows alongside n, table size (n * W) grows quadratically.")
    print("  - Nearest Neighbor TSP takes the most time because it executes Dijkstra")
    print("    from each stop (k + 1 times) before selecting the O(k^2) greedy tour,")
    print("    which is still far faster than exact exponential O(k!) TSP.")

    print("\n5. Generated Runtime Charts:")
    print(f"  - Individual Scaling Chart : {chart_paths[0]}")
    print(f"  - Comparison Chart         : {chart_paths[1]}")


def run_performance_analysis(output_dir=CHARTS_DIR):
    """Run all benchmarks, generate Matplotlib charts, and print the report."""
    print("\nRunning performance benchmarks using time.perf_counter()...")
    individual_data = benchmark_individual_algorithms()
    comparison_data = benchmark_common_comparison()
    chart_paths = generate_charts(individual_data, comparison_data, output_dir)
    print_performance_report(individual_data, comparison_data, chart_paths)
