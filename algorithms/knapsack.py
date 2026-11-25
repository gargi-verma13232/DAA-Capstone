"""
algorithms/knapsack.py - Optimal Parcel Selection using 0/1 Knapsack (DP).

Each parcel has an integer weight and priority (value).
Selects a subset of parcels maximizing total priority within vehicle capacity.

Complexity:
  - Time Complexity : O(n * W)
  - Space Complexity: O(n * W)
"""

from algorithms.sorting import display_parcels_table


def knapsack_01(parcels, capacity):
    """
    Solve the 0/1 Knapsack problem manually using bottom-up Dynamic Programming.

    Returns a dictionary with:
      - dp_table: 2D list of size (n + 1) x (capacity + 1)
      - selected: list of selected parcels
      - rejected: list of rejected parcels
      - total_weight: sum of weights of selected parcels
      - total_value: sum of priority values of selected parcels
      - capacity: maximum allowed capacity
    """
    n = len(parcels)
    if capacity < 0:
        raise ValueError("Vehicle capacity cannot be negative.")

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        parcel_weight = parcels[i - 1]["weight"]
        parcel_value = parcels[i - 1]["priority"]

        for w in range(1, capacity + 1):
            if parcel_weight <= w:
                include_val = parcel_value + dp[i - 1][w - parcel_weight]
                exclude_val = dp[i - 1][w]
                dp[i][w] = include_val if include_val > exclude_val else exclude_val
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    rejected = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= parcels[i - 1]["weight"]
        else:
            rejected.append(parcels[i - 1])

    selected.reverse()
    rejected.reverse()

    total_weight = sum(p["weight"] for p in selected)
    total_value = sum(p["priority"] for p in selected)

    if total_weight > capacity:
        raise ValueError("Knapsack invariant violated: total weight exceeds capacity.")

    return {
        "dp_table": dp,
        "selected": selected,
        "rejected": rejected,
        "total_weight": total_weight,
        "total_value": total_value,
        "capacity": capacity,
    }


def display_dp_table(dp_table, parcels, capacity):
    """Display the 0/1 Knapsack DP table cleanly."""
    print("\n--- 0/1 Knapsack DP Table (Rows = Parcels, Cols = Capacity 0..W) ---")
    if capacity > 30:
        print(f"(Capacity W={capacity} is large; showing first 15 and last 5 columns)")
        cols = list(range(0, 15)) + list(range(capacity - 4, capacity + 1))
    else:
        cols = list(range(0, capacity + 1))

    header = f"{'Parcel':<10} | " + " ".join(f"{c:>3}" for c in cols)
    print(header)
    print("-" * len(header))

    for i in range(len(dp_table)):
        row_label = "0 (None)" if i == 0 else parcels[i - 1]["id"]
        row_vals = " ".join(f"{dp_table[i][c]:>3}" for c in cols)
        print(f"{row_label:<10} | {row_vals}")


def display_knapsack_result(result, parcels, show_table=True):
    """Display DP table, selected parcels, rejected parcels, and packing summary."""
    if show_table:
        display_dp_table(result["dp_table"], parcels, result["capacity"])

    print(f"\nVehicle Maximum Capacity: {result['capacity']} kg")
    display_parcels_table(result["selected"], "Selected Parcels (Optimal Load)")
    display_parcels_table(result["rejected"], "Rejected Parcels")

    print("\n--- Packing Summary ---")
    print(f"  Selected Count : {len(result['selected'])} / {len(parcels)}")
    print(f"  Total Weight   : {result['total_weight']} kg (Limit: {result['capacity']} kg)")
    print(f"  Total Value    : {result['total_value']}")
    within_limit = result["total_weight"] <= result["capacity"]
    print(f"  Capacity Check : {'PASSED (Within Limit)' if within_limit else 'FAILED'}")

    print("\nAlgorithm Analysis (0/1 Knapsack DP):")
    print("  - Time Complexity : O(n * W)")
    print("  - Space Complexity: O(n * W)")
