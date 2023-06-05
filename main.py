import networkx as nx


Edge = tuple[object, object, object]
Node = object


class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        nx.MultiDiGraph.__init__(self, incoming_graph_data=None, multigraph_input=None, **attr)
        self.rotor_order = dict()


    def simple_path(n: int = 5):
        graph = RotorGraph()
        for i in range(1, n-1):
            graph.add_edge(i, i-1)
            graph.add_edge(i, i+1)

        return graph


    def add_edge(self, u_for_edge: Node, v_for_edge: Node, key=None, **attr) -> object:
        """
        Add an edge to the graph with MultiDiGraph method and update the rotor order
        Input:
            - u_for_edge: tail node
            - v_for_edge: head node
            - key: identifier (default=lowest unused integer)
            - attr: keyword arguments, optional
        Output:
            The edge key assigned to the edge.
        """
        key = nx.MultiDiGraph.add_edge(self, u_for_edge, v_for_edge, key=None, **attr)
        edge = (u_for_edge, v_for_edge, key)
        if u_for_edge in self.rotor_order.keys():
            self.rotor_order[u_for_edge].append(edge)
        else:
            self.rotor_order[u_for_edge] = [edge]
        return key


    def head(self, edge: Edge) -> Node:
        """
        Return the head's value of an edge if it exist
        else return None
        Input:
            - edge: tuple identifying an edge
        Output:
            - head's value of the edge
        """
        if edge in self.edges:
            return edge[1]
        else: return None


    def tail(self, edge: Edge) -> Node:
        """
        Return the tail's value of an edge if it exist
        else return None
        Input:
            - edge: tuple identifying an edge
        Output:
            - tail's value of the edge
        """
        if edge in self.edges:
            return edge[0]
        else: return None


    def set_rotor_order(self, new_order: dict[Node, list(Edge)]):
        """
        Define the rotor order to consider.
        The new order will override the old one of the given nodes.
        Each node needs all its outgoing edges.
        Input:
            - new_order: dict of the form {node: [edges]}
        No output
        """
        for node, edges in new_order.items():
            if node not in self.nodes:
                raise KeyError(f"Invalid node '{node}'")

            for edge in edges:
                if edge not in self.edges:
                    raise ValueError(f"Invalid edge {edge}")
                
                if node != self.tail(edge):
                    raise ValueError(f"The node '{node}' does not correspond to the tail of the edge {edge}")
            
            if self.out_degree(node) != len(edges):
                raise ValueError(f"Not all edges of the node '{node}' are given")

        self.rotor_order.update(new_order)


    def invert_rotor_order(self):
        """
        Invert the rotor order of the graph.
        No input
        No output
        """
        for node in self.rotor_order:
            self.rotor_order[node].reverse()


def turn(self, edges: list(Edge)):
    pass


def main():
    G = RotorGraph.simple_path()
    print(G.rotor_order)


if __name__ == "__main__":
    main()
