import copy
from typing import List, Dict
from pathlib import Path

import networkx as nx
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
        self._routes = routes
        self._stations = stations
        self._companies = companies
        self.graph = self._init_network_graph()

    def _init_network_graph(self, routes = None, stations = None):
        """
        Method for loading in the routing information into a networkx graph.
        That graph can then be used to determine the different pathing options.
        """
        if stations is None:
            stations = self._stations
        if routes is None:
            routes = self._routes

        graph = nx.MultiGraph()
        self._load_nodes(stations, graph=graph)
        self._load_routes(routes, graph=graph)

        return graph

    def _load_nodes(self, stations: Dict, graph = None):
        """
        Loads a set of nodes into the local graph.
        """
        if graph is None:
            graph = self.graph

        for key, values in stations.items():
            graph.add_node(key, **values)

        return graph

    def _load_routes(self, routes: List[Dict], graph = None):
        """
        Loads a set of routes into the existing network graph.
        It is expected that the nodes have already been loaded using _load_nodes.
        Failure to do so will result in missing metadata.
        """
        if graph is None:
            graph = self.graph

        for route in routes:
            route_metadata = copy.deepcopy(route)
            route_metadata.pop('start_station')
            route_metadata.pop('end_station')
            graph.add_edge(route['start_station'],
                           route['end_station'],
                           **route_metadata)
        return graph

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
