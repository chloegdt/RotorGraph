# RotorGraph

Table of contents :bookmark:
- [RotorGraph](#Rotorgraph)
- [Results](#Results)
- [ParticleConfig](#ParticleConfig)
- [RotorConfig](#RotorConfig)
- [Vector](#Vector)

## RotorGraph(class) ##
Simulate a rotor graph from the networkx.MultiDiGraph class
Methods:
* **simple_path(n=5, x=1, y=1)**, create a simple path RotorGraph with **n** nodes, **x** left edges, **y** right edges and 2 sinks (extremities)
* **grid(n: int=3, m: int=3, sinks: str="")**, create a grid RotorGraph with **n** rows and **m** columns, sinks &in; {"borders", "corners", "center"}
* **random_graph(min_nb_nodes:int=5, max_nb_nodes:int=15)**, create a random RotorGraph with n nodes, n &in; [min_nb_nodes..max_nb_nodes]
* **remove_edge(self, *edges: Edge)**, remove given edges (e.g. G.remove_edge(e1, e2, e3) or G.remove_edge(e1))
* **set_sink(self, \*nodes: Node)**, set given nodes as sink
* **remove_sink(self, \*nodes: Node)**, unset given nodes as sink
* **head(self, edge: Edge)**, return head of edge
* **tail(self, edge: Edge)**, return tail of edge
* **set_rotor_order(self, new_order: dict[Node, list(Edge)])**, set the rotor order of the RotorGraph
* **invert_rotor_order(self)**, invert the rotor order
* **check_rotor_config(self, rotor_config: RotorConfig):**, Check if the given rotor configuration is valid for the RotorGraph
* **turn(self, edge: Edge, k: int=1)**, Give the next edge of the given edge in rotor order
* **turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None) -> RotorConfig:**, Turn all edges of the configuration
* **reverse_turn(self, edge: Edge, k: int=1)**, Give the previous edge of the given edge in rotor order
* **reverse_turn_all(self, rotor_config: RotorConfig, k: int=1, sinks: set=None)**, Turn all edges of the configuration in the reverse order
* **step(self, particle_config: object, rotor_config: RotorConfig, node: Node=None, sinks: set=None, turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig)**, Make one step of routing
* **reverse_step(self, particle_config: object, rotor_config: RotorConfig, node:Node=None, sinks: set=None, turn_and_move: bool=False, info=None) -> (ParticleConfig, RotorConfig)**, Make one step of routing in reverse
* **legal_routing(self, particle_config: object, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route particles to the sinks
* **route_one_particle(self, node: Node, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> RotorConfig**, Route one particule from the given node to a sink
* **complete_routing(self, particle_config: ParticleConfig, rotor_config: RotorConfig, sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route particles and antiparticles to the sinks
* **laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]**, Create the laplacian matrix of the graph
* **reduced_laplacian_matrix(self, sinks: set=None) -> dict[Node, dict[Node, int]]**, Create the reduced laplacian matrix of the graph
* **vector_routing(self, particle_config: object, rotor_config: RotorConfig, vector: dict[Node:int], sinks: set=None, turn_and_move: bool=False) -> (ParticleConfig, RotorConfig)**, Route the graph according to a given vector optimized with the laplacian matrix
* **enum_configurations(self, sinks:set=None) -> list[RotorConfig]**, Gives a list of all the rotor configuration of the graph
* **enum_acyclic_configurations(self, sinks:set=None) -> list[RotorConfig]**, Gives a list of all the acyclic rotor configuration of the graph where each represents a class
* **recurrent_from_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]**, For all acyclic configuration, gives the corresponding recurrent configuration in the class
* **recurrent_and_acyclic(self, list_acyclic:list[RotorConfig]) -> list[tuple[RotorConfig, RotorConfig]]**, For all acyclic configuration, gives the corresponding recurrent configuration in the class

## Results

## ParticleConfig

## RotorConfig

## Vector
