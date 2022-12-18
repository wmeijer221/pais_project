from typing import List, Dict
from pathlib import Path

import yaml


class RouteDatabase:
    """
    Object that holds and constructs a network graph of all known routes.
    Can also be asked to generate routes based on certain criteria.
    """
    def __init__(self, routes: List[Dict], stations: Dict, companies: Dict):
        """
        Creates a route database, loading it into a graph from a list.
        """
        self.routes = routes
        self.stations = stations
        self.companies = companies

    @classmethod
    def from_file(cls, file_path: Path):
        """
        Creates a route database by loading routes and stations from a file.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        with open(file_path, "r") as file_descriptor:
            file_contents: str = file_descriptor.read()
            railway_data = yaml.load(file_contents, Loader=yaml.SafeLoader)

        return cls(railway_data["routes"], railway_data["stations"], railway_data["companies"])