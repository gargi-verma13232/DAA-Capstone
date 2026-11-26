"""
data/sample_data.py - JSON data loader for parcel and location datasets.
"""

import json
import os


DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PARCELS_JSON = os.path.join(DATA_DIR, "parcels.json")
LOCATIONS_JSON = os.path.join(DATA_DIR, "locations.json")


def load_sample_data():
    """Load parcels, vehicle capacity, depot, locations, and roads from JSON files."""
    with open(PARCELS_JSON, "r", encoding="utf-8") as pf:
        parcel_data = json.load(pf)

    with open(LOCATIONS_JSON, "r", encoding="utf-8") as lf:
        location_data = json.load(lf)

    roads = [tuple(edge) for edge in location_data["roads"]]
    return (
        parcel_data["parcels"],
        parcel_data["vehicle_capacity"],
        location_data["depot"],
        location_data["locations"],
        roads,
    )
