class Results(object):

    def __init__(self, graph, particle_config, rotor_config):
        self.nb_steps = 0
        self.nb_l_edges = 0
        self.nb_r_edges = 0
        self.edges_counter = {edge:0 for edge in graph.edges}
        self.nodes_counter = {node:0 for node in graph.nodes}
        self.nb_particles_in_sinks = {sink:particle_config[sink] for sink in graph.sinks}
        self.last_visit = {node:None for node in graph.nodes}
        self.configuration_history = [(rotor_config, particle_config)]
        

    def __str__(self):
        res = f"Number of steps : {self.nb_steps}\n"
        if (self.nb_l_edges != 0) or (self.nb_r_edges != 0):
            res += f"Number of left edges : {self.nb_l_edges} \nNumber of right edges : {self.nb_r_edges}\n\n"
        res += " Node | visits | last_visit | nb_particles | sink \n"
        particle_config = self.configuration_history[-1][-1]
        f = " {0:>4} | {1:>6} | {2:>10} | {3:>12} | "
        for node in self.nodes_counter:
            #res += f"  {node}   |   {self.nodes_counter[node]}    | {self.last_visit[node]}      | {particle_config[node]} | "
            res += f.format(node, self.nodes_counter[node], str(self.last_visit[node]), particle_config[node])
            if node in self.nb_particles_in_sinks:
                res += "yes\n"
            else: 
                res += "no\n"
        res += "\n"    
        for edge in self.edges_counter:
            res += f"Edge {edge} : {self.edges_counter[edge]}\n"

        return res

    def orientation_edges(self, rotor_config):

        for edge in rotor_config.values():
            if edge[0] == (edge[1] + 1):
                self.nb_l_edges += 1
            if edge[0] == (edge[1] - 1):
                self.nb_r_edges += 1


    def particles_in_sinks(self, particle_config):

        for sink in self.nb_particles_in_sinks:
            self.nb_particles_in_sinks[sink] = particle_config[sink]



