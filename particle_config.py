class ParticleConfig(Vector):

    def __init__(self, configuration:dict=None):
        if isinstance(configuration, dict):
            self.configuration = configuration
        elif isinstance(configuration, RotorGraph):
            self.configuration = {node: 0 for node in configuration}
        elif configuration is None:
            self.configuration = dict()
        else:
            raise TypeError("configuration has to be a dict, RotorGraph or nothing")


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