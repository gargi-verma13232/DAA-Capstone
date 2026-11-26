# Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (`ETCCDA302`) — Capstone Assignment  
**Institution:** K.R. Mangalam University, Gurugram, Haryana  
**Language:** Python (with Matplotlib for runtime charts)

---

## 1. Problem Statement

Mini-Courier Planner simulates an intelligent courier delivery planning system. Given a list of parcels (with weight, priority, deadline, and destination) and a weighted road network graph starting from a central `Depot`, the application:

1. Prioritizes parcels using **Merge Sort**.
2. Selects the optimal parcel combination within vehicle capacity using **0/1 Knapsack (Dynamic Programming)**.
3. Computes shortest road paths from the depot and between delivery stops using **Dijkstra's Algorithm**.
4. Generates a delivery route and total travel distance using **Nearest Neighbor TSP** (an approximation algorithm).
5. Benchmarks all four algorithms using `time.perf_counter()` across small and large inputs and generates runtime comparison charts.

---

## 2. Project Structure

```text
Mini-Courier-Planner/
├── main.py
├── requirements.txt
├── README.md
├── algorithms/
│   ├── sorting.py
│   ├── knapsack.py
│   ├── dijkstra.py
│   └── tsp.py
├── data/
│   ├── parcels.json
│   ├── locations.json
│   └── sample_data.py
├── performance/
│   └── performance_analysis.py
├── tests/
│   └── test_algorithms.py
└── results/
    ├── runtime_charts/
    │   ├── runtime_individual.png
    │   └── runtime_comparison.png
    └── screenshots/
```

---

## 3. Implemented Algorithms & Complexity

| Step | Algorithm | File | Time Complexity | Space Complexity | Role in System |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Merge Sort** | `algorithms/sorting.py` | $O(n \log n)$ | $O(n)$ | Sorts parcels by priority (descending) and deadline (ascending); stable sort |
| 2 | **0/1 Knapsack DP** | `algorithms/knapsack.py` | $O(n \cdot W)$ | $O(n \cdot W)$ | Builds $(n+1)\times(W+1)$ DP table and selects optimal parcels within capacity $W$ |
| 3 | **Dijkstra's Algorithm** | `algorithms/dijkstra.py` | $O((V + E) \log V)$ | $O(V + E)$ | Finds shortest paths & distances on weighted graph; marks unreachable nodes |
| 4 | **Nearest Neighbor TSP** | `algorithms/tsp.py` | $O(k(V + E)\log V + k^2)$ | $O(k^2 + V + E)$ | Greedy **approximation** tour visiting all $k$ stops using Dijkstra distances and returning to `Depot` |

---

## 4. Integrated Workflow (8 Steps)

When running **Complete Courier Plan** (Menu Option `6`):

1. Load sample parcel data (`10` parcels, vehicle capacity `25 kg`) and location graph (`10` locations, `14` weighted roads) from `data/parcels.json` and `data/locations.json` via `data/sample_data.py`.
2. Sort parcels using `merge_sort_parcels` by priority descending, then deadline ascending.
3. Apply `knapsack_01` to select the maximum-priority subset of parcels with total weight $\le 25\text{ kg}$.
4. Extract unique delivery locations from the selected parcels (`extract_delivery_locations`).
5. Run `dijkstra` from `Depot` to compute shortest distances and paths (identifying `Remote-Outpost` as unreachable).
6. Run `nearest_neighbor_tsp` over Dijkstra shortest-path distances to generate the delivery route starting and ending at `Depot`.
7. Sum all leg distances to compute the total delivery route distance.
8. Display the consolidated final courier plan.

---

## 5. How to Run

### Prerequisites

- Python 3.x
- `matplotlib` (listed in `requirements.txt`)

### Setup & Execution Commands

```powershell
cd Mini-Courier-Planner
pip install -r requirements.txt
python main.py
```

### Run Unit & Integration Tests

```powershell
python -m unittest tests.test_algorithms -v
```

---

## 6. Menu Options

```text
1. Display Parcels
2. Sort Parcels
3. Optimal Parcel Selection (Knapsack)
4. Shortest Path (Dijkstra)
5. Delivery Route (Nearest Neighbor TSP)
6. Complete Courier Plan
7. Performance Analysis
8. Exit
```

---

## 7. Sample Execution Results

On the sample dataset (`10` parcels, `vehicle_capacity = 25 kg`):

- **Selected Parcels (6):** `P103`, `P109`, `P110`, `P102`, `P108`, `P106`
- **Rejected Parcels (4):** `P105`, `P101`, `P107`, `P104`
- **Total Loaded Weight:** `25 kg / 25 kg` (within capacity)
- **Total Priority Value:** `380`
- **Unreachable Node Handling (Dijkstra):** `Remote-Outpost` reported as `Unreachable`
- **Delivery Sequence (Nearest Neighbor TSP):**
  `Depot -> Sector-14 -> Cyber-Hub -> Udyog-Vihar -> Palam-Vihar -> Sohna-Road -> Depot`
- **Total Route Distance:** `52 km`

---

## 8. Performance Analysis & Optimization Notes

Option `7` runs `performance/performance_analysis.py` using `time.perf_counter()` across small and large synthetic datasets and saves two charts inside `results/runtime_charts/`:

- `results/runtime_charts/runtime_individual.png` — Individual scaling plots for each algorithm.
- `results/runtime_charts/runtime_comparison.png` — Side-by-side comparison across common input sizes $N \in \{10, 25, 50, 75, 100\}$.

### Observed Behavior & Future Optimizations

- **Merge Sort & Dijkstra** scale smoothly as $O(n \log n)$ and $O((V + E) \log V)$, staying fast even for thousands of parcels or vertices.
- **0/1 Knapsack DP** scales pseudo-polynomially as $O(n \cdot W)$, making it sensitive to large vehicle capacities. If the DP table does not need to be displayed, space complexity can be reduced from $O(n \cdot W)$ to $O(W)$ using a 1D rolling array (or meet-in-the-middle for small $n$ and very large $W$).
- **Nearest Neighbor TSP** is the slowest step in combined scaling because it runs Dijkstra from each stop ($k + 1$ times) before the $O(k^2)$ tour selection, though it remains vastly faster than exact $O(k!)$ TSP. Route quality can be improved further by adding a **2-opt** local search pass after Nearest Neighbor construction.
