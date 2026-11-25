"""
algorithms/tsp.py - Delivery Route Planning using Nearest Neighbor TSP.

NOTE: Nearest Neighbor TSP is a greedy APPROXIMATION algorithm.
It uses shortest-path distances obtained from Dijkstra's Algorithm to
select the nearest unvisited delivery stop at each step and return to depot.

Complexity:
  - Time Complexity : O(k * (V + E) log V + k^2) for k delivery stops
  - Space Complexity: O(k^2 + V + E)
"""

from algorithms.dijkstra import dijkstra, reconstruct_path


def extract_delivery_locations(selected_parcels, depot):
    """
    Extract unique delivery locations from selected parcels (excluding depot)
    and group parcels by their destination location.
    """
    locations = []
    parcels_by_location = {}

    for parcel in selected_parcels:
        loc = parcel["location"]
        if loc == depot:
            continue
        if loc not in parcels_by_location:
            locations.append(loc)
            parcels_by_location[loc] = []
        parcels_by_location[loc].append(parcel)

    return locations, parcels_by_location


def nearest_neighbor_tsp(graph, depot, delivery_locations):
    """
    Construct a delivery tour starting and ending at `depot` by greedily
    selecting the nearest unvisited stop using Dijkstra shortest paths.
    """
    if not delivery_locations:
        return {
            "route_stops": [depot],
            "legs": [],
            "total_distance": 0,
            "unreachable_stops": [],
        }

    stops_to_compute = [depot] + list(delivery_locations)
    shortest_from = {}
    for stop in stops_to_compute:
        shortest_from[stop] = dijkstra(graph, stop)

    unvisited = list(delivery_locations)
    unreachable_stops = []
    route_stops = [depot]
    legs = []
    total_distance = 0
    current = depot

    while unvisited:
        distances, parents = shortest_from[current]
        nearest_loc = None
        nearest_dist = float("inf")

        for candidate in unvisited:
            cand_dist = distances.get(candidate, float("inf"))
            if cand_dist < nearest_dist:
                nearest_dist = cand_dist
                nearest_loc = candidate

        if nearest_loc is None or nearest_dist == float("inf"):
            unreachable_stops.extend(unvisited)
            break

        road_path = reconstruct_path(parents, current, nearest_loc)
        legs.append({
            "from": current,
            "to": nearest_loc,
            "distance": nearest_dist,
            "road_path": road_path,
        })
        total_distance += nearest_dist
        route_stops.append(nearest_loc)
        unvisited.remove(nearest_loc)
        current = nearest_loc

    if current != depot:
        distances, parents = shortest_from[current]
        return_dist = distances.get(depot, float("inf"))
        if return_dist != float("inf"):
            road_path = reconstruct_path(parents, current, depot)
            legs.append({
                "from": current,
                "to": depot,
                "distance": return_dist,
                "road_path": road_path,
            })
            total_distance += return_dist
            route_stops.append(depot)
        else:
            unreachable_stops.append(f"Return to {depot}")

    return {
        "route_stops": route_stops,
        "legs": legs,
        "total_distance": total_distance,
        "unreachable_stops": unreachable_stops,
    }


def display_tsp_route(tsp_result, parcels_by_location=None):
    """Display Nearest Neighbor TSP sequence, leg paths, and total distance."""
    print("\n--- Delivery Route (Nearest Neighbor TSP - Approximation Algorithm) ---")
    print("Note: Nearest Neighbor TSP is a greedy APPROXIMATION algorithm.")
    print("      It uses Dijkstra shortest-path distances between delivery stops.")

    stops = tsp_result["route_stops"]
    print("\nFinal Delivery Sequence:")
    print("  " + " -> ".join(stops))

    print("\nStep-by-Step Route Breakdown (via Dijkstra Shortest Paths):")
    if not tsp_result["legs"]:
        print("  No delivery trips required.")
    else:
        for idx, leg in enumerate(tsp_result["legs"], start=1):
            road_str = " -> ".join(leg["road_path"])
            parcel_info = ""
            if parcels_by_location and leg["to"] in parcels_by_location:
                ids = ", ".join(p["id"] for p in parcels_by_location[leg["to"]])
                parcel_info = f" | Deliver: [{ids}]"
            elif idx == len(tsp_result["legs"]) and leg["to"] == stops[0]:
                parcel_info = " | Return to Depot"
            print(
                f"  Step {idx}: {leg['from']} -> {leg['to']} "
                f"({leg['distance']} km) | Road Path: {road_str}{parcel_info}"
            )

    if tsp_result["unreachable_stops"]:
        print(f"\nWarning - Unreachable Stops: {', '.join(tsp_result['unreachable_stops'])}")

    print(f"\nTotal Delivery Route Distance: {tsp_result['total_distance']} km")
    print("\nAlgorithm Analysis (Nearest Neighbor TSP):")
    print("  - Algorithm Type  : Approximation / Greedy Heuristic (not guaranteed globally optimal)")
    print("  - Time Complexity : O(k^2) for tour selection + O(k * (V + E) log V) for Dijkstra")
    print("  - Space Complexity: O(k^2 + V + E)")
