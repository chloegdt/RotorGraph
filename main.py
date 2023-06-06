import networkx as nx


Edge = tuple[object, object, object]
Node = object
RotorConfig = dict[Node, Edge]

class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        nx.MultiDiGraph.__init__(self)
        mg = nx.MultiDiGraph(incoming_graph_data, multigraph_input, **attr)
        self.edges = mg.edges
        self.nodes = mg.nodes
        self.sinks = set()
        self.rotor_order = {edge[0]: [e for e in self.edges if e[0] == edge[0]] for edge in self.edges}


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


    def set_sink(self, *nodes: Node):
        self.sinks.update(nodes)



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



    def check_rotor_config(self, rotor_config: RotorConfig):
        """
        Check if the given rotor configuration is valid for the RotorGraph
        Input:
            - rotor_config: Dict containg the rotor configuration to check
        No output but raises en error if the configuration is not valid.
        """
        for node, edge in rotor_config.items():
            if node not in self.nodes:
                raise KeyError(f"Invalid node '{node}'")

            if edge not in self.edges:
                raise ValueError(f"Invalid edge {edge}")
                
            if node != self.tail(edge):
                raise ValueError(f"The node '{node}' does not correspond to the tail of the edge {edge}")


    def turn(self, edge: Edge, k: int=1):
        """
        Give the next edge of the given edge in rotor order
        Input:
            - edge: Edge to turn k times
            - k: number of times to turn (default: one time)
        Output:
            - Resulting Edge after the turn
        """
        if edge not in self.edges:
            raise ValueError(f"Invalid edge {edge}")

        order = self.rotor_order[edge[0]]
        n = len(order)
        if (n == 1) or (k%n == 0):
            return edge
        
        current_idx = order.index(edge)
        next_idx = (current_idx + k) % n
        
        return order[next_idx]


class ParticleConfig:

    def __init__(self, configuration:dict=None):
        if configuration is None:
            self.configuration = dict()
        else:
            self.configuration = configuration

    def __str__(self):
        return repr(self.configuration)

    def __add__(self, other):
        x = self.configuration
        y = other.configuration
        print(x)
        print(y)
        res_dic = {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
        for k in set(x) | set(y):
            a = x.get(k,0)
            b = y.get(k,0)
            print(f"{a} + {b} = {a+b}")
        return ParticleConfig(res_dic)

    def add_particles(self, node:Node, k:int=1):
        if node in self.configuration:
            self.configuration[node] += k
        else: self.configuration[node] = k

    def remove_particles(self, node:Node, k:int=1):
        if node in self.configuration:
            self.configuration[node] -= k
        else: self.configuration[node] = -k

    def set_particles(self, node:Node, k:int=1):
        self.configuration[node] = k


def main():
    G = RotorGraph.simple_path()
    x = ParticleConfig()
    x.add_particles(1,5)
    x.add_particles(2,4)
    x.add_particles(3,7)
    y = ParticleConfig()
    y.add_particles(1)
    y.add_particles(3,9)
    print(x)
    print(y)
    z = x + y
    print(z.configuration)


if __name__ == "__main__":
    main()
