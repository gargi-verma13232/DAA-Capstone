"""
main.py - Mini-Courier Planner (DAA Capstone Assignment)

Integrates all four algorithms in a menu-driven terminal application:
  1. Merge Sort               (Parcel Prioritization)
  2. 0/1 Knapsack DP          (Optimal Parcel Selection)
  3. Dijkstra's Algorithm     (Shortest Paths)
  4. Nearest Neighbor TSP     (Delivery Route Approximation)
"""

from algorithms.sorting import (
    merge_sort_parcels,
    display_parcels_table,
    display_sorting_result,
)
from algorithms.knapsack import knapsack_01, display_knapsack_result
from algorithms.dijkstra import (
    build_graph,
    dijkstra,
    display_graph,
    display_shortest_paths,
)
from algorithms.tsp import (
    extract_delivery_locations,
    nearest_neighbor_tsp,
    display_tsp_route,
)
from data.sample_data import load_sample_data
from performance.performance_analysis import run_performance_analysis


def run_complete_courier_plan():
    """
    Execute the complete 8-step integrated courier planning pipeline:
      1. Load parcel and location data.
      2. Sort parcels based on priority/deadline (Merge Sort).
      3. Apply 0/1 Knapsack to select parcels according to vehicle capacity.
      4. Extract delivery locations of selected parcels.
      5. Apply Dijkstra's Algorithm to calculate shortest paths.
      6. Apply Nearest Neighbor TSP to generate the delivery route.
      7. Calculate total delivery distance.
      8. Display the final courier plan.
    """
    print("\n============================================================")
    print("             COMPLETE INTEGRATED COURIER PLAN               ")
    print("============================================================")

    parcels, capacity, depot, locations, roads = load_sample_data()
    graph = build_graph(locations, roads)
    print(f"\n[Step 1] Data Loaded: {len(parcels)} parcels, Capacity = {capacity} kg, Depot = '{depot}'")

    print("\n[Step 2] Sorting Parcels (Merge Sort)...")
    sorted_parcels = merge_sort_parcels(parcels)
    display_parcels_table(sorted_parcels, "Prioritized Parcels (Sorted)")

    print("\n[Step 3] Selecting Optimal Parcels (0/1 Knapsack DP)...")
    knapsack_result = knapsack_01(sorted_parcels, capacity)
    display_knapsack_result(knapsack_result, sorted_parcels, show_table=False)

    selected_parcels = knapsack_result["selected"]
    delivery_locations, parcels_by_location = extract_delivery_locations(selected_parcels, depot)
    print("\n[Step 4] Extracted Delivery Locations from Selected Parcels:")
    if delivery_locations:
        for loc in delivery_locations:
            ids = ", ".join(p["id"] for p in parcels_by_location[loc])
            print(f"  - {loc} (Parcels: {ids})")
    else:
        print("  No delivery locations to visit.")

    print("\n[Step 5] Calculating Shortest Paths from Depot (Dijkstra's Algorithm)...")
    distances, parents = dijkstra(graph, depot)
    display_shortest_paths(graph, depot, distances, parents)

    print("\n[Step 6 & 7] Generating Delivery Route (Nearest Neighbor TSP)...")
    tsp_result = nearest_neighbor_tsp(graph, depot, delivery_locations)
    display_tsp_route(tsp_result, parcels_by_location)

    print("\n[Step 8] === FINAL COURIER PLAN SUMMARY ===")
    print(f"  Starting Depot       : {depot}")
    print(f"  Vehicle Capacity     : {capacity} kg")
    print(f"  Selected Parcels     : {len(selected_parcels)} ({', '.join(p['id'] for p in selected_parcels)})")
    print(f"  Total Loaded Weight  : {knapsack_result['total_weight']} kg / {capacity} kg")
    print(f"  Total Priority Value : {knapsack_result['total_value']}")
    print(f"  Delivery Sequence    : {' -> '.join(tsp_result['route_stops'])}")
    print(f"  Total Route Distance : {tsp_result['total_distance']} km")
    print("============================================================")


def print_menu():
    """Display the main terminal menu."""
    print("\n========================================")
    print("         MINI-COURIER PLANNER           ")
    print("========================================")
    print("1. Display Parcels")
    print("2. Sort Parcels")
    print("3. Optimal Parcel Selection (Knapsack)")
    print("4. Shortest Path (Dijkstra)")
    print("5. Delivery Route (Nearest Neighbor TSP)")
    print("6. Complete Courier Plan")
    print("7. Performance Analysis")
    print("8. Exit")
    print("========================================")


def main():
    """Run the interactive menu-driven Mini-Courier Planner application."""
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            parcels, capacity, depot, locations, roads = load_sample_data()
            display_parcels_table(parcels, f"All Parcels (Vehicle Capacity: {capacity} kg)")
            print(f"\nDepot: {depot} | Total Locations in Network: {len(locations)} | Roads: {len(roads)}")

        elif choice == "2":
            parcels, _, _, _, _ = load_sample_data()
            sorted_parcels = merge_sort_parcels(parcels)
            display_sorting_result(parcels, sorted_parcels)

        elif choice == "3":
            parcels, capacity, _, _, _ = load_sample_data()
            sorted_parcels = merge_sort_parcels(parcels)
            result = knapsack_01(sorted_parcels, capacity)
            display_knapsack_result(result, sorted_parcels, show_table=True)

        elif choice == "4":
            _, _, depot, locations, roads = load_sample_data()
            graph = build_graph(locations, roads)
            display_graph(graph)
            distances, parents = dijkstra(graph, depot)
            display_shortest_paths(graph, depot, distances, parents)

        elif choice == "5":
            parcels, capacity, depot, locations, roads = load_sample_data()
            graph = build_graph(locations, roads)
            sorted_parcels = merge_sort_parcels(parcels)
            knapsack_result = knapsack_01(sorted_parcels, capacity)
            delivery_locations, parcels_by_location = extract_delivery_locations(
                knapsack_result["selected"], depot
            )
            print(
                f"\nRouting {len(knapsack_result['selected'])} selected parcels "
                f"(Total Weight: {knapsack_result['total_weight']}/{capacity} kg):"
            )
            tsp_result = nearest_neighbor_tsp(graph, depot, delivery_locations)
            display_tsp_route(tsp_result, parcels_by_location)

        elif choice == "6":
            run_complete_courier_plan()

        elif choice == "7":
            run_performance_analysis()

        elif choice == "8":
            print("\nExiting Mini-Courier Planner. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
