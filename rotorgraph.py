import networkx as nx
from types_definition import * 
from unionfind import UnionFind
from copy import deepcopy
import rotorconfig
import particleconfig
from random import randint

class RotorGraph(nx.MultiDiGraph):

    def __init__(self, incoming_graph_data=None, multigraph_input=None, **attr):
        self.sinks = set()
        self.rotor_order = dict()
        self.edge_index = dict()
        nx.MultiDiGraph.__init__(self, incoming_graph_data, multigraph_input, **attr)
        # self.rotor_order = {edge[0]: [e for e in self.edges if e[0] == edge[0]] for edge in self.edges}


    def simple_path(n: int = 5) -> RotorGraph:
        """
        Create a simple path rotor graph with n nodes including two sinks at the extremities 
        Input:
            - n: the number of nodes in the graph (default : five nodes)
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


    def grid(n: int=3, m: int=3, sinks: str="") -> RotorGraph:
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

        sinks = sinks.lower()
        if sinks in {"border", "borders"}:
            for i in range(n):
                graph.set_sink()
            for i in range(m):
                graph.set_sink(i, i*m, i*m + m-1, (n-1)*m+i)

        elif sinks in {"corner", "corners"}:
            graph.set_sink(0, m-1, n*m, m*(n-1), m*n-1)
        elif sinks in {"center"}:
            graph.set_sink((n*m) // 2)

        return graph

    def random_graph(min_nb_nodes=5, max_nb_nodes=15) -> RotorGraph:
        G = RotorGraph()
        nb_nodes = randint(min_nb_nodes, max_nb_nodes)
        for i in range(nb_nodes):
            G.add_edge(i, i+1)
            #G.add_edge(i+1, i)

        for _ in range(randint(nb_nodes//2, 2*nb_nodes+1)):
            u = randint(0, nb_nodes)
            v = randint(0, nb_nodes+1)
            G.add_edge(u, v)

        
        G.add_edge(nb_nodes, nb_nodes+1)
        G.set_sink(nb_nodes+1)
        for i in range(3):
            G.set_sink(randint(0, nb_nodes))
        

        return G


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


    def turn(self, edge: Edge, k: int=1) -> Edge:
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

    
    def reverse_turn(self, edge: Edge, k: int=1) -> Edge:
        """
        Give the previous edge of the given edge in rotor order
        Input:
            - edge: Edge to turn k times
            - k: number of times to turn (default: one time)
        Output:
            - resulting Edge after the turn
        """
        if edge not in self.edges:
            raise ValueError(f"Invalid edge {edge}")

        order = self.rotor_order[edge[0]]
        n = len(order)
        if (n == 1) or (k%n == 0):
            return edge
        
        current_idx = self.edge_index[edge]
        previous_idx = (current_idx - k) % n
        
        return order[previous_idx]

    def reverse_turn_all(self, rotor_config: RotorConfig, sinks: set=None) -> RotorConfig:
        """
        Turn all edges of the configuration in the reverse order 
        Input:
            - rotor_config: the rotor configuration to turn
            - k: number of times to turn (default: one time)
        Output:
            - new resulting Config after the turn
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks

        res_config = deepcopy(rotor_config)
        for node in rotor_config.configuration.keys():
            res_config.configuration[node] = self.reverse_turn(rotor_config.configuration[node])

        return res_config
            

    def step(self, particle_config: object, rotor_config: RotorConfig, node: Node=None, sinks: set=None,
             turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
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
            if node == None: return particle_config, rotor_config

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
             turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
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
            if node == None: return particle_config, rotor_config

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
                      turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
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
                    matrix[u][v] = self.out_degree(u) - self.number_of_edges(u, v)
                else:
                    matrix[u][v] = -self.number_of_edges(u, v)

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
                    matrix[u][v] = self.out_degree(u) - self.number_of_edges(u, v)
                else:
                    matrix[u][v] = -self.number_of_edges(u, v)

        return matrix


    def vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector:
                       dict[Node:int], sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig):
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


    def enum_acyclic_configurations(self, sinks:set=None) -> list[set[Edge]]:
        """
        Gives a list of all the acyclic rotor configuration of the graph where each represents a
        class
        Input:
            - sinks: set of nodes that are considered as sinks
        Output:
            - list of acyclic configurations (set of edges)
        """
        if sinks == None:
            if self.sinks:
                sinks = self.sinks
            else:
                raise Exception("No sink in the graph: cannot find an acyclic configuration.")

        nodes = [node for node in self.rotor_order.keys() if node not in sinks]
        i = 0 # index of the node where to chose the next edge
        acyclic_config = list() # resulting list
        rotor_configuration = [0 for _ in range(len(nodes))] # take first edges of all nodes
        uf_list = [None for _ in range(len(nodes))] # set unionfind list
        uf_list[0] = UnionFind(list(self.nodes)) # create the first unionfind

        while rotor_configuration[0] < self.out_degree(nodes[0]):
            if i == len(nodes)-1: # last node
                if rotor_configuration[i] < self.out_degree(nodes[i]): # not his last edge
                    # check if adding the edge will not create a cycle
                    edge = self.rotor_order[nodes[i]][rotor_configuration[i]]
                    if not uf_list[i].connected(edge[0], edge[1]):
                        dic = {nodes[i]: self.rotor_order[nodes[i]][rotor_configuration[i]] for i in range(len(nodes))}
                        rc = rotorconfig.RotorConfig(dic)
                        acyclic_config.append(rc)
                    rotor_configuration[i] += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1

            else:
                if rotor_configuration[i] < self.out_degree(nodes[i]):
                    edge = self.rotor_order[nodes[i]][rotor_configuration[i]]
                    if not uf_list[i].connected(edge[0], edge[1]):
                        uf_list[i+1] = deepcopy(uf_list[i])
                        uf_list[i+1].union(edge[0], edge[1])
                        i += 1
                    else:
                        rotor_configuration[i] += 1
                else:
                    rotor_configuration[i] = 0
                    i -= 1
                    rotor_configuration[i] += 1
        return acyclic_config



    def recurrent_and_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]:
        """
        For all acyclic configuration, gives the corresponding recurrent configuration in the class
        Input:
            - list_acyclic: the list of all acyclic configuration of the graph
        Output:
            - list of tuples (recurrent configuration, acyclic configuration)
        """
        rec_acyclic = list()
        for config in list_acyclic:
            rec = self.reverse_turn_all(config)
            acy = deepcopy(rec)
            acy.destination_forest(self)
            rec_acyclic.append((rec, acy))

        return rec_acyclic


def all_config_from_recurrent(rotor_graph: RotorGraph, rotor_config: RotorConfig, sinks:set=None,
                              set_config: set[RotorConfig]=None) -> set[RotorConfig]:
    """
    Gives all the configuration in the class of the given recurrent configuration
    Input:
        - rotor_graph: the RotorGraph of the recurrent configuration
        - rotor_config: the recurrent RotorConfig of the class
        - sinks: a set of Node to consider as sink
        - set_config: the set where to store the RotorConfig
    Output:
        - set of all the RotorConfig of the class
    """
    if set_config == None:
        set_config = {rotor_config}
        if sinks == None:
            if rotor_graph.sinks:
                sinks = rotor_graph.sinks

    if cycles := rotor_config.find_cycles(sinks):
        for cycle in cycles:
            next_config = deepcopy(rotor_config)
            next_config.cycle_push(rotor_graph, cycle)
            set_config.add(next_config)
            all_config_from_recurrent(rotor_graph, next_config, sinks, set_config)
    return set_config



def display_path(rotor_config: RotorConfig, particle_config: ParticleConfig=None):
    """
    Give a graphical representation in the terminal of a simple path graph configuration.
    Input:
        - particle_config: the particule configuration of the graph
        - rotor_config: the rotor configuration of the graph
    No output
    """
    if particle_config == None:
        n = len(rotor_config.configuration) + 2
        particle_config = particleconfig.ParticleConfig({i:"x" for i in range(n)})

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


def display_grid(rotor_config: RotorConfig, n, m, particle_config: ParticleConfig=None):
    """
    Give a graphical representation in the terminal of a simple path graph configuration.
    Input:
        - particle_config: the particule configuration of the graph
        - rotor_config: the rotor configuration of the graph
    No output
    """
    if particle_config == None:
        particle_config = particleconfig.ParticleConfig({i:"x" for i in range(n*m)})

    for j in range(n):
        for i in range(j*m, j*m+m-1):
            print(particle_config.configuration[i],end='')
            if (i+1, i, 0) in rotor_config.configuration.values():
                print('<',end='')
            else: print(' ',end='')
            print('-',end='')
            if (i, i+1, 0) in rotor_config.configuration.values():
                print('>',end='')
            else: print(' ',end='')
        print(particle_config.configuration[j*m+m-1], end='')
        print()
        if j < n-1:
            for i in range(j*m, j*m+m-1):
                if (i+m, i, 0) in rotor_config.configuration.values():
                    print('^',end='')
                else: print(' ',end='')
                print('   ',end='')
            if (i+m, i, 0) in rotor_config.configuration.values():
                print('^',end='')
            else: print(' ',end='')
            print()
            for i in range(j*m, j*m+m-1):
                print("|   ", end='')
            print('|', end='')
            print()
            for i in range(j*m, j*m+m-1):
                if (i, i+m, 0) in rotor_config.configuration.values():
                    print('v',end='')
                else: print(' ',end='')
                print('   ',end='')
            if (i, i+m, 0) in rotor_config.configuration.values():
                print('v',end='')
            else: print(' ',end='')
            print()


def rotor_order2edge_index(rotor_order: dict[Node, list[Edge]]) -> dict[Edge, int]:
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
