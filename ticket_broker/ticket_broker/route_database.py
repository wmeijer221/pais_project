import copy
from typing import List, Dict
from pathlib import Path

import logging
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
        self.companies = companies
        self._init_network_graph()

    def find_route_options(self, start_station, end_station, weight):
        """
        Finds a route from one station to another.

        start_station: The station to start the journey.
        end_station: The station to end the journey.
        weight: the name of the edge weight to use. Look in railways.yaml for the metadata with each route.

        return: a list of journey options, each journey is a dict with the following keys:
            - label : display name for the form UI
            - value : the individual legs in the route. This item is named in such a way to ensure compatibility with
                      the radio button in CAMUNDA forms, which expects this key.
        For now, we only return one option.
        """
        intermediate_stations = nx.shortest_path(self.graph, start_station, end_station, weight=weight)

        journey = {
            "label": f"Journey from {start_station} to {end_station} consisting of: \n"
        }

        legs = []
        for i in range(len(intermediate_stations) - 1):
            leg_start = intermediate_stations[i]
            leg_end = intermediate_stations[i + 1]

            leg_data = {"start_station": leg_start,
                        "end_station": leg_end}

            leg_data.update(self._select_best_leg(leg_start, leg_end, weight))
            legs.append(leg_data)

            journey["label"] += f"Leg from {leg_start} to {leg_end} with {leg_data['company']}\n"

        journey["value"] = legs

        return [journey]

    def _select_best_leg(self, leg_start, leg_end, weight):
        """
        Selects the best option for a certain leg of the journey,
        based on the weight condition. Will select the smallest weight.
        """
        edges = self.graph.get_edge_data(leg_start, leg_end)

        logging.debug(f"LEG DATA FROM {leg_start} to {leg_end}:\n EDGES: {edges}")

        if len(edges) == 1:
            best_option = 0
        else:
            # If we have multiple choices for one leg, we choose the right one by the weight
            best_option = 0
            best_weight_value = edges[0][weight]
            for key, edge in edges.items():
                if edge[weight] < best_weight_value:
                    best_option = key

        return edges[best_option]

    def _init_network_graph(self, routes=None, stations=None):
        """
        Method for loading in the routing information into a networkx graph.
        That graph can then be used to determine the different pathing options.
        """
        if stations is None:
            stations = self._stations
        if routes is None:
            routes = self._routes

        self.graph = nx.MultiGraph()
        self._load_nodes(stations)
        self._load_routes(routes)

        return self.graph

    def _load_nodes(self, stations: Dict):
        """
        Loads a set of nodes into the local graph.
        """
        for key, values in stations.items():
            self.graph.add_node(key, **values)

        return self.graph

    def _load_routes(self, routes: List[Dict]):
        """
        Loads a set of routes into the existing network graph.
        It is expected that the nodes have already been loaded using _load_nodes.
        Failure to do so will result in missing metadata.
        """

        for route in routes:
            route_metadata = copy.deepcopy(route)
            route_metadata.pop('start_station')
            route_metadata.pop('end_station')
            self.graph.add_edge(route['start_station'],
                           route['end_station'],
                           **route_metadata)
        return self.graph

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
