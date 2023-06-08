import networkx as nx


Edge = tuple[object, object, object]
Node = object
RotorConfig = dict[Node, Edge]
Sinks = set

class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        self.sinks = set()
        self.rotor_order = dict()
        nx.MultiDiGraph.__init__(self, incoming_graph_data, multigraph_input, **attr)
        # self.rotor_order = {edge[0]: [e for e in self.edges if e[0] == edge[0]] for edge in self.edges}


    def simple_path(n: int = 5):
        graph = RotorGraph()
        for i in range(n): graph.add_node(i)
        for i in range(1, n-1):
            graph.add_edge(i, i-1)
            graph.add_edge(i, i+1)
        graph.set_sink(0, n-1)

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
        
        current_idx = order.index(edge)
        next_idx = (current_idx + k) % n
        
        return order[next_idx]

    def step(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None,
             turn_and_move: bool=False):
        """
        Make one step of routing
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
        # retrieve sinks
        if sinks == None: sinks = self.sinks
 
        # get node
        node = particle_config.first_node_with_particle(sinks)
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


    def vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector: dict, sinks: set=None):
        matrix = self.reduced_laplacian_matrix(sinks)
        for u, c in vector.items():

            for v, p in matrix[u].items():
                particle_config.configuration[v] -= c*p









class RotorConfig:

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










class ParticleConfig:

    def __init__(self, configuration:dict=None):
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif isinstance(configuration, RotorGraph):
            self.configuration = {node: 0 for node in configuration}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")

    def __str__(self):
        return repr(self.configuration)

    def __add__(self, other: object or int) -> object:
        """
        Overload the + operator.
        Case: ParticleConfig + ParticleConfig
            for each node, do the sum of the particles in both configurations
        Case: ParticleConfig + integer
            for each node, add the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k + other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __radd__(self, other: object or int) -> object:
        """
        Same method as __add__ except that it makes the + operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) + config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k + other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __sub__(self, other: object or int) -> object:
        """
        Overload the - operator.
        Case: ParticleConfig - ParticleConfig
            for each node, do the substraction of the particles in both configurations
        Case: ParticleConfig - integer
            for each node, substract the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: particle configuration or integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, ParticleConfig):
            config2 = other.configuration
            res_dic = {n: config1.get(n, 0) - config2.get(n, 0) for n in set(config1) | set(config2)}
        elif isinstance(other, int):
            res_dic = {n: k - other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int or a ParticleConfig")
        return ParticleConfig(res_dic)

    def __mul__(self, other: int) -> object:
        """
        Overload the * operator.
        Case: ParticleConfig * integer
            for each node, multiply the integer to the number of particles
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __rmul__(self, other: int) -> object:
        """
        Same method as __mul__ except that it makes the * operator commutative. 
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k * other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __truediv__(self, other: int) -> object:
        """
        Overload the / operator.
        Case: ParticleConfig / integer
            for each node, divide the number of particles by an integer
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)

    def __floordiv__(self, other: int) -> object:
        """
        Overload the // operator.
        Case: ParticleConfig // integer
            for each node, divide the number of particles by an integer
        Input: 
            - self: particle configuration
            - other: integer
        Ouput:
            - new particle configuration
        """
        config1 = self.configuration
        if isinstance(other, int):
            res_dic = {n: k // other for n, k in config1.items()}
        else:
            raise TypeError("Second operand must be an int")
        return ParticleConfig(res_dic)



    def first_node_with_particle(self, sinks: set):
        """
        Find the first (non sink) node which holds at least one particle
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - the first non sink node with at least one particle if there is one
            else None
        """
        for node, k in self.configuration.items():
            if k > 0 and node not in sinks:
                return node
        return None

    def transfer_particles(self, u: Node, v: Node, k: int=1):
        """
        Transfer k particles from node u to node v
        Input:
            - u: node giving the k particles
            - v: node receiving the k particles
            - k: the number of particles to transfer (default: one particle)
        No output
        """
        self.configuration[u] -= k
        self.configuration[v] += k

    def add_particles(self, node:Node, k:int=1):
        """
        Add the number of particles on the given node
        Input:
            - node: the node where to add k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        if node in self.configuration:
            self.configuration[node] += k
        else: self.configuration[node] = k

    def remove_particles(self, node:Node, k:int=1):
        """
        Remove the number of particles on the given node
        Input:
            - node: the node where to remove k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        if node in self.configuration:
            self.configuration[node] -= k
        else: self.configuration[node] = -k

    def set_particles(self, node:Node, k:int=1):
        """
        Set the number of particles on the given node
        Input:
            - node: the node where to set k particles 
            - k: the number of particles (default: one particle)
        No output
        """
        self.configuration[node] = k




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







def main():
    G = RotorGraph.simple_path()
    sigma = ParticleConfig(G)
    sigma += 2
    rho = RotorConfig(G)

    print(sigma)
    print(rho)

    sigma, rho = G.legal_routing(sigma, rho)

    print(sigma)
    print(rho)



if __name__ == "__main__":
    main()
