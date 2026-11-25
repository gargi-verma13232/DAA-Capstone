"""
algorithms/sorting.py - Parcel Prioritization using Merge Sort.

Sorting Rule:
  1. Higher priority comes first (descending order).
  2. Equal priority is broken by earlier deadline (ascending order).

Complexity:
  - Best / Average / Worst Time Complexity: O(n log n)
  - Auxiliary Space Complexity: O(n)
  - Stability: Stable
"""


def comes_before(parcel_a, parcel_b):
    """Return True if parcel_a should appear before parcel_b."""
    if parcel_a["priority"] != parcel_b["priority"]:
        return parcel_a["priority"] > parcel_b["priority"]
    return parcel_a["deadline"] <= parcel_b["deadline"]


def merge(left, right):
    """Merge two sorted parcel lists into a single sorted list."""
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if comes_before(left[i], right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def merge_sort_parcels(parcels):
    """Sort parcels manually using Merge Sort and return a new sorted list."""
    if len(parcels) <= 1:
        return list(parcels)

    mid = len(parcels) // 2
    left_half = merge_sort_parcels(parcels[:mid])
    right_half = merge_sort_parcels(parcels[mid:])
    return merge(left_half, right_half)


def display_parcels_table(parcels, title):
    """Display a list of parcels in a formatted table."""
    print(f"\n--- {title} ---")
    if not parcels:
        print("No parcels to display.")
        return

    header = f"{'ID':<8} {'Weight(kg)':<12} {'Priority':<10} {'Deadline(hr)':<14} {'Location':<18}"
    print(header)
    print("-" * len(header))
    for p in parcels:
        print(
            f"{p['id']:<8} {p['weight']:<12} {p['priority']:<10} "
            f"{p['deadline']:<14} {p.get('location', 'N/A'):<18}"
        )


def display_sorting_result(unsorted_parcels, sorted_parcels):
    """Display unsorted vs sorted parcels and algorithm complexities."""
    display_parcels_table(unsorted_parcels, "Unsorted Parcels")
    display_parcels_table(sorted_parcels, "Sorted Parcels (Priority Desc, Deadline Asc)")

    print("\nSorting Order (Top Priority -> Lowest Priority):")
    order_str = " -> ".join(
        f"{p['id']}(P:{p['priority']}, D:{p['deadline']}h)" for p in sorted_parcels
    )
    print(" ", order_str)

    print("\nAlgorithm Analysis (Merge Sort):")
    print("  - Best / Average / Worst Time Complexity: O(n log n)")
    print("  - Space Complexity: O(n) auxiliary space")
    print("  - Stable Sorting Algorithm: Yes")
