"""
tests/test_algorithms.py - Unit and integration tests for Mini-Courier Planner.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.sorting import merge_sort_parcels
from algorithms.knapsack import knapsack_01
from algorithms.dijkstra import build_graph, dijkstra, reconstruct_path
from algorithms.tsp import extract_delivery_locations, nearest_neighbor_tsp
from data.sample_data import load_sample_data


class TestMiniCourierAlgorithms(unittest.TestCase):
    def test_merge_sort_priority_and_deadline_tiebreak(self):
        sample = [
            {"id": "A", "weight": 3, "priority": 50, "deadline": 6, "location": "L1"},
            {"id": "B", "weight": 2, "priority": 80, "deadline": 5, "location": "L2"},
            {"id": "C", "weight": 4, "priority": 80, "deadline": 2, "location": "L3"},
        ]
        sorted_list = merge_sort_parcels(sample)
        self.assertEqual([p["id"] for p in sorted_list], ["C", "B", "A"])
        self.assertEqual([p["id"] for p in sample], ["A", "B", "C"])

    def test_knapsack_respects_capacity_and_optimality(self):
        parcels, capacity, _, _, _ = load_sample_data()
        sorted_parcels = merge_sort_parcels(parcels)
        result = knapsack_01(sorted_parcels, capacity)

        self.assertLessEqual(result["total_weight"], capacity)
        self.assertEqual(result["total_weight"], 25)
        self.assertEqual(result["total_value"], 380)
        self.assertEqual(len(result["dp_table"]), len(sorted_parcels) + 1)
        self.assertEqual(len(result["dp_table"][0]), capacity + 1)
        self.assertEqual(
            len(result["selected"]) + len(result["rejected"]),
            len(sorted_parcels),
        )

    def test_dijkstra_shortest_paths_and_unreachable(self):
        _, _, depot, locations, roads = load_sample_data()
        graph = build_graph(locations, roads)
        distances, parents = dijkstra(graph, depot)

        self.assertEqual(distances["Depot"], 0)
        self.assertEqual(distances["Sector-14"], 4)
        self.assertEqual(distances["Cyber-Hub"], 10)
        self.assertEqual(reconstruct_path(parents, depot, "Cyber-Hub"), ["Depot", "MG-Road", "Cyber-Hub"])
        self.assertEqual(distances["Remote-Outpost"], float("inf"))
        self.assertEqual(reconstruct_path(parents, depot, "Remote-Outpost"), [])

    def test_nearest_neighbor_tsp_and_full_integration(self):
        parcels, capacity, depot, locations, roads = load_sample_data()
        graph = build_graph(locations, roads)

        sorted_parcels = merge_sort_parcels(parcels)
        knapsack_result = knapsack_01(sorted_parcels, capacity)
        delivery_locs, _ = extract_delivery_locations(knapsack_result["selected"], depot)
        tsp_result = nearest_neighbor_tsp(graph, depot, delivery_locs)

        self.assertEqual(tsp_result["route_stops"][0], depot)
        self.assertEqual(tsp_result["route_stops"][-1], depot)
        for loc in delivery_locs:
            self.assertIn(loc, tsp_result["route_stops"])
        self.assertEqual(tsp_result["unreachable_stops"], [])
        self.assertEqual(tsp_result["total_distance"], 52)


if __name__ == "__main__":
    unittest.main()
