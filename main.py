import networkx as nx


class RotorGraph(nx.MultiDiGraph):

    def head(self, edge: int) -> object:
        """
        Return the head's value of an edge if it exist
        else return None
        Input:
            - edge: integer identifying an edge
        Output:
            - head's value of the edge
        """
        edges = list(self.edges())
        if edge >= len(edges):
            return None
        else:
            return edges[edge][1]


    def tail(self, edge: int) -> object:
        """
        Return the tail's value of an edge if it exist
        else return None
        Input:
            - edge: integer identifying an edge
        Output:
            - tail's value of the edge
        """
        edges = list(self.edges())
        if edge >= len(edges):
            return None
        else:
            return edges[edge][0]


def main():
    G = RotorGraph()
    G.add_edge('a',4)
    print(G.tail(0))
    print(G.tail(1))


if __name__ == "__main__":
    main()
