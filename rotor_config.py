class RotorConfig(Vector):

    def __init__(self, configuration: dict or RotorGraph=None):
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif isinstance(configuration, RotorGraph):
            self.configuration = {node: edges[0] for node, edges in configuration.rotor_order.items()}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")

    def __str__(self):
        return repr(self.configuration)

    def __repr__(self):
        return repr(self.configuration)

    def find_cycles(self, sinks: set[Node]=set()) -> list[list[Edge]]:
        """
        Find all cycles from a rotor configuration
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - list cycle
        """
        visited_nodes = set()
        cycles = list()

        for node in self.configuration:
            cycle = list()
            while (node not in visited_nodes) and (node not in sinks) and (node in self.configuration):
                edge = self.configuration[node]
                cycle.append(edge)
                visited_nodes.add(node)
                node = edge[1]
            while cycle and cycle[0][0] != cycle[-1][1]:
                del cycle[0]

            if cycle and cycle[0][0] == cycle[-1][1]:
                cycles.append(cycle)

        return cycles

    def to_graph(self):
        """doc"""
        subgraph = RotorGraph()
        for edge in self.configuration.values():
            subgraph.add_edge(edge)

        return subgraph


    def cycle_pushing(self, rotor_graph: RotorGraph, sinks: set[Node]=set()):
        """
        Cycle push algorithm
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - new rotor configuration without cycle
        """
        while cycles := self.find_cycles(sinks):
            for cycle in cycles:
                for edge in cycle:
                    self.configuration[edge[0]] = rotor_graph.turn(edge)






