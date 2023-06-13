import networkx as nx
from types_definition import * 

class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        self.sinks = set()
        self.rotor_order = dict()
        self.edge_index = dict()
        nx.MultiDiGraph.__init__(self, incoming_graph_data, multigraph_input, **attr)
        # self.rotor_order = {edge[0]: [e for e in self.edges if e[0] == edge[0]] for edge in self.edges}


    def simple_path(n: int = 5):
        """
        Create a simple path rotor graph with n nodes including two sinks at the extremities 
        Input:
            - n : the number of nodes in the graph (default : five nodes)
        Output:
            - a simple path rotor graph
        """
        graph = RotorGraph()
        for i in range(n): graph.add_node(i)
        for i in range(1, n-1):
            graph.add_edge(i, i-1)
            graph.add_edge(i, i+1)
        graph.set_sink(0, n-1)

        return graph


    def grid(n: int=3, m: int=3):
        """
        Create a grid rotor graph n*m nodes
        Input:
            - n: number of rows 
            - m: number of columns
        Output:
            - a grid rotor graph
        """
        graph = RotorGraph()
        total_nodes = n*m
        for i in range(total_nodes): graph.add_node(i)
        for i in range(n):
            for j in range(m):
                node = i*m + j
                if (node-m) in range(total_nodes): graph.add_edge(node, node-m)
                if (j+1) in range(m): graph.add_edge(node, node+1)
                if (node+m) in range(total_nodes): graph.add_edge(node, node+m)
                if (j-1) in range(m): graph.add_edge(node, node-1)

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
            self.edge_index[edge] = len(self.rotor_order[u_for_edge]) - 1
        else:
            self.rotor_order[u_for_edge] = [edge]
            self.edge_index[edge] = 0
        return key


    def set_sink(self, *nodes: Node):
        """
        Set the given nodes as a sink
        Input:
            - nodes: multiple Node to set as sink
        No output
        """
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
            
            if self.out_degree(node) != len(set(edges)):
                raise ValueError(f"Not all edges of the node '{node}' are given")

        self.rotor_order.update(new_order)
        self.edge_index = rotor_order2edge_index(self.rotor_order)

    def invert_rotor_order(self):
        """
        Invert the rotor order of the graph.
        No input
        No output
        """
        for node in self.rotor_order:
            self.rotor_order[node].reverse()
        self.edge_index = rotor_order2edge_index(self.rotor_order)


    def check_rotor_config(self, rotor_config: RotorConfig):
        """
        Check if the given rotor configuration is valid for the RotorGraph
        Input:
            - rotor_config: Dict containg the rotor configuration to check
        No output but raises en error if the configuration is not valid.
        """
        for node, edge in rotor_config.configuration.items():
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
        
        current_idx = self.edge_index[edge]
        next_idx = (current_idx + k) % n
        
        return order[next_idx]

    def step(self, particle_config: object, rotor_config: RotorConfig, node: Node=None, sinks: set=None,
             turn_and_move: bool=False):
        """
        Make one step of routing
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - node: the node where to make a step (default: the first non sink node with a particle)
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then move
        Output:
            - new particle configuration
            - new rotor configuration
        """
        # retrieve sinks
        if sinks == None: sinks = self.sinks
 
        # get node
        if node == None:
            # try to find the fist non sink node with a particle
            node = particle_config.first_node_with_particle(sinks)

            # if no node given or found: nothing changes
            if node == None: return particle_config

        if turn_and_move:
            # turn
            rotor_config.configuration[node] = self.turn(edge)

            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(node, succ)

        else: # move and turn
            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(node, succ)

            # turn
            rotor_config.configuration[node] = self.turn(edge)

        return particle_config, rotor_config

    def reverse_step(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None,
             turn_and_move: bool=False):
        """
        Make one step of routing in reverse
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - node: the node where to make a reverse step (default: the first non sink node with a particle)
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then move
        Output:
            - new particle configuration
            - new rotor configuration
        """
        # retrieve sinks
        if sinks == None: sinks = self.sinks
 
        # get node
        node = particle_config.first_node_with_particle(sinks)
        if node == None:
            # try to find the fist non sink node with a particle
            node = particle_config.first_node_with_particle(sinks)

            # if no node given or found: nothing changes
            if node == None: return particle_config

        if turn_and_move:
            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(succ, node)

            # turn
            rotor_config.configuration[node] = self.turn(edge)

        else: # move and turn
            # turn
            rotor_config.configuration[node] = self.turn(edge)

            # move
            edge = rotor_config.configuration[node]
            succ = self.head(edge)
            particle_config.transfer_particles(succ, node)

        return particle_config, rotor_config

    def legal_routing(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None,
                      turn_and_move: bool=False) -> object and RotorConfig:
        """
        Route particles to the sinks
        Input:
            - particle_config: the particle configuration of the graph
            - rotor_config: the rotor configuration of the graph
            - sinks: set of nodes that are considered as sinks (optional)
            - turn_and_move: boolean (default: False),
                if True: turn first then move
                else (False): move first then move
        Output:
            - new particle configuration
            - new rotor configuration
        """
        if sinks is None and len(self.sinks) == 0:
            print("Infinite loop")
            return

        if sinks == None:
            sinks = self.sinks

        while particle_config.first_node_with_particle(sinks) != None:
            # display_path(particle_config, rotor_config) # debug only
            particle_config, rotor_config = self.step(particle_config, rotor_config, sinks,
                                                      turn_and_move)

        return particle_config, rotor_config



    def step_one_particle(self, node: Node, rotor_config: RotorConfig):
        """A VOIR"""
        pass

    def laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]:
        """
        Create the laplacian matrix of the graph
        Input:
            - sinks: set of nodes that are considered as sinks (optional)
        Output : 
            - the laplacian matrix of the graph (dict of dict)
        """
        if sinks is None:
            non_sink_nodes = self.nodes - self.sinks
        else:
            non_sink_nodes = self.nodes - sinks

        matrix = dict()
        for u in non_sink_nodes:
            matrix[u] = dict()
            for v in self.nodes:
                if u == v:
                    matrix[u][v] = self.out_degree(u)
                else:
                    if self.has_edge(u, v):
                        matrix[u][v] = -1
                    else:
                        matrix[u][v] = 0

        return matrix

    def reduced_laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]:
        """
        Create the reduced laplacian matrix of the graph
        Input:
            - sinks: set of nodes that are considered as sinks (optional)
        Output : 
            - the reduced laplacian matrix of the graph (dict of dict)
        """
        if sinks is None:
            nodes = self.nodes - self.sinks
        else:
            nodes = self.nodes - sinks

        matrix = dict()
        for u in nodes:
            matrix[u] = dict()
            for v in nodes:
                if u == v:
                    matrix[u][v] = self.out_degree(u)
                else:
                    if self.has_edge(u, v):
                        matrix[u][v] = -1
                    else:
                        matrix[u][v] = 0

        return matrix


    def vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector:
                       dict[Node:int], sinks: set=None, turn_and_move: bool=False) -> object and RotorConfig:
        """
        Route the graph according to a given vector optimized with the laplacian matrix
        Input:
            - particle_config : the particle configuration of the graph
            - rotor_config : the rotor configuration of the graph
            - vector : dict[Node:int]
            - sinks : set of nodes that are considered as sinks
            - turn_and_move : boolean (default=False)
                if True: turn first then move
                else (False): move first then turn
        Output:
            - the new particle configuration
            - the new rotor configuration
        """
        matrix = self.laplacian_matrix(sinks)
        for u, k in vector.items():
            if u not in matrix: continue

            c = k // matrix[u][u]

            for v, p in matrix[u].items():
                particle_config.configuration[v] -= c*p

            for _ in range(k % matrix[u][u]):
                self.step(particle_config, rotor_config, node=u, sinks=sinks, turn_and_move=turn_and_move)

        return particle_config, rotor_config




def display_path(particle_config: ParticleConfig, rotor_config: RotorConfig):
    """
    Give a graphical representation in the terminal of a simple path graph configuration.
    Input:
        - particle_config: the particule configuration of the graph
        - rotor_config: the rotor configuration of the graph
    No output
    """
    for i in range(len(particle_config.configuration)-1):
        print(particle_config.configuration[i],end='')
        if (i+1, i, 0) in rotor_config.configuration.values():
            print('<',end='')
        else: print(' ',end='')
        print('-',end='')
        if (i, i+1, 0) in rotor_config.configuration.values():
            print('>',end='')
        else: print(' ',end='')
    print(particle_config.configuration[len(particle_config.configuration)-1])


def rotor_order2edge_index(rotor_order: dict[Node, list[Edge]]) -> dict:
    """
    Give the position of the edges in the given rotor order  
    Input :
        - rotor_order: the rotor order to convert
    Output:
        - dict[Edge: index in rotor order]
    """
    dic = dict()
    for node, edges in rotor_order.items():
        for edge in edges:
            dic[edge] = edges.index(edge)

    return dic
