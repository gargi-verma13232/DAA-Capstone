"""
algorithms/dijkstra.py - Shortest Path Calculation using Dijkstra's Algorithm.

Complexity:
  - Time Complexity : O((V + E) log V)
  - Space Complexity: O(V + E)
"""

import heapq


def build_graph(locations, roads):
    """Build an undirected weighted adjacency-list graph from locations and roads."""
    graph = {loc: [] for loc in locations}
    for u, v, dist in roads:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, dist))
        graph[v].append((u, dist))
    return graph


def dijkstra(graph, source):
    """
    Compute shortest distances and parent pointers from `source` using
    Dijkstra's Algorithm. Unreachable nodes retain distance float('inf').
    """
    distances = {node: float("inf") for node in graph}
    parents = {node: None for node in graph}
    visited = set()

    if source not in graph:
        return distances, parents

    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        curr_dist, curr_node = heapq.heappop(priority_queue)

        if curr_node in visited:
            continue
        visited.add(curr_node)

        for neighbor, weight in graph[curr_node]:
            if neighbor in visited:
                continue
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parents[neighbor] = curr_node
                heapq.heappush(priority_queue, (new_dist, neighbor))

    return distances, parents


def reconstruct_path(parents, source, target):
    """Reconstruct shortest path [source, ..., target], or [] if unreachable."""
    if source == target:
        return [source]

    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            break
        current = parents.get(current)

    path.reverse()
    if not path or path[0] != source:
        return []
    return path


def display_graph(graph):
    """Display the weighted road network graph."""
    print("\n--- Road Network (Weighted Graph Adjacency List) ---")
    for node, edges in graph.items():
        if edges:
            edge_str = ", ".join(f"{nbr} ({w} km)" for nbr, w in edges)
        else:
            edge_str = "No connecting roads (Isolated / Unreachable)"
        print(f"  {node:<18} -> {edge_str}")


def display_shortest_paths(graph, source, distances, parents):
    """Display shortest distances and paths from source, handling unreachable nodes."""
    print(f"\n--- Shortest Paths from '{source}' (Dijkstra's Algorithm) ---")
    header = f"{'Destination':<18} {'Distance(km)':<15} {'Shortest Path'}"
    print(header)
    print("-" * (len(header) + 25))

    for loc in graph:
        dist = distances[loc]
        if dist == float("inf"):
            print(f"{loc:<18} {'Unreachable':<15} No path available from {source}")
        else:
            path = reconstruct_path(parents, source, loc)
            print(f"{loc:<18} {dist:<15} {' -> '.join(path)}")

    print("\nAlgorithm Analysis (Dijkstra's Algorithm):")
    print("  - Time Complexity : O((V + E) log V)")
    print("  - Space Complexity: O(V + E)")
