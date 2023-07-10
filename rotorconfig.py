from types_definition import *
import rotorgraph


class RotorConfig(object):

    def __init__(self, configuration: dict or RotorGraph=None):
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif isinstance(configuration, rotorgraph.RotorGraph):
            self.configuration = {node: edges[0] for node, edges in configuration.rotor_order.items()}
        elif type(configuration).__name__ == "Vector":
            self.configuration = {edge[0]: edge for edge, value in configuration.items() if value}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")

    def __str__(self):
        return repr(self.configuration)

    def __repr__(self):
        return repr(self.configuration)

    def items(self):
        return self.configuration.items()
    
    def keys(self):
        return self.configuration.keys()

    def values(self):
        return self.configuration.values()

    def __setitem__(self, index:object, value:object):
        """
        Overload the assignement operator.
        Set the value in dict at the given index.
        Input: 
            - self: RotorConfig
            - index: dictionnary key
            - value: value to store
        No ouput
        """
        self.configuration[index] = value

    def __getitem__(self, index: object):
        """
        Overload the getter operator.
        Return the value in dict at the given index.
        Input: 
            - self: RotorConfig
            - index: dictionnary key
        Output:
            - the value at the given index
        """
        return self.configuration.get(index, 0)

    def __delitem__(self, index: object):
        """
        Overload the deleter operator.
        Input:
            - self: RotorConfig
            - index: dictinnay key
        No output
        """
        del self.configuration[index]

    def __len__(self) -> int:
        """
        doc
        """
        return len(self.configuration)

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

    def to_graph(self) -> RotorGraph:
        """
        Gives the corresponding RotorGraph of the RotorConfig
        Input: None
        Output:
            - rotor graph of the RotorConfig
        """
        subgraph = rotorgraph.RotorGraph()
        for edge in self.configuration.values():
            subgraph.add_edge(edge[0], edge[1])

        return subgraph

    def cycle_push(self, rotor_graph: RotorGraph, cycle: list[Edge]):
        """
        Turn all of the given edges in the RotorConfig
        Input:
            - cycle: a list of edges to turn
        Output: None
        """
        for edge in cycle:
            self.configuration[edge[0]] = rotor_graph.turn(edge)


    def destination_forest(self, rotor_graph: RotorGraph, sinks: set[Node]=set()):
        """
        The configuration obtained by a maximal cycle push sequence on a rotor configuration 
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - new rotor configuration without cycle
        """
        while cycles := self.find_cycles(sinks):
            for cycle in cycles:
                self.cycle_push(rotor_graph, cycle)


