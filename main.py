import networkx as nx


Edge = tuple[object, object, object]
Node = object
RotorConfig = dict[Node, Edge]
Sinks = set


def main():
    G = RotorGraph.grid(2,2)
    v = Vector()


if __name__ == "__main__":
    main()
