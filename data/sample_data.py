"""
data/sample_data.py - Sample parcel and location datasets for Mini-Courier Planner.
"""

VEHICLE_CAPACITY = 25

PARCELS = [
    {"id": "P101", "weight": 6, "priority": 85, "deadline": 2, "location": "Sector-14"},
    {"id": "P102", "weight": 4, "priority": 60, "deadline": 5, "location": "Cyber-Hub"},
    {"id": "P103", "weight": 7, "priority": 90, "deadline": 1, "location": "Sohna-Road"},
    {"id": "P104", "weight": 5, "priority": 50, "deadline": 6, "location": "MG-Road"},
    {"id": "P105", "weight": 8, "priority": 95, "deadline": 2, "location": "Golf-Course-Road"},
    {"id": "P106", "weight": 3, "priority": 40, "deadline": 8, "location": "Udyog-Vihar"},
    {"id": "P107", "weight": 9, "priority": 75, "deadline": 4, "location": "Sector-56"},
    {"id": "P108", "weight": 2, "priority": 55, "deadline": 3, "location": "Cyber-Hub"},
    {"id": "P109", "weight": 5, "priority": 70, "deadline": 4, "location": "Palam-Vihar"},
    {"id": "P110", "weight": 4, "priority": 65, "deadline": 5, "location": "Sector-14"},
]

DEPOT = "Depot"

LOCATIONS = [
    "Depot",
    "Sector-14",
    "Cyber-Hub",
    "Sohna-Road",
    "MG-Road",
    "Golf-Course-Road",
    "Udyog-Vihar",
    "Sector-56",
    "Palam-Vihar",
    "Remote-Outpost",
]

ROADS = [
    ("Depot", "Sector-14", 4),
    ("Depot", "MG-Road", 6),
    ("Depot", "Palam-Vihar", 9),
    ("Sector-14", "MG-Road", 3),
    ("Sector-14", "Cyber-Hub", 7),
    ("Sector-14", "Sohna-Road", 8),
    ("MG-Road", "Cyber-Hub", 4),
    ("MG-Road", "Golf-Course-Road", 5),
    ("Cyber-Hub", "Udyog-Vihar", 3),
    ("Cyber-Hub", "Palam-Vihar", 6),
    ("Golf-Course-Road", "Sector-56", 4),
    ("Golf-Course-Road", "Sohna-Road", 6),
    ("Sohna-Road", "Sector-56", 5),
    ("Udyog-Vihar", "Palam-Vihar", 5),
]


def load_sample_data():
    """Return fresh copies of sample parcels, vehicle capacity, depot, locations, and roads."""
    parcels_copy = [dict(p) for p in PARCELS]
    return parcels_copy, VEHICLE_CAPACITY, DEPOT, list(LOCATIONS), list(ROADS)
