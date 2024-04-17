import networkx as nx

from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from adhoccomputing.Generics import *

from bracha_toueg.BrachaTouegCrashConsensusAlgorithmComponentModel import (
    BrachaTouegCrashConsensusAlgorithmComponentModel,
)
from bracha_toueg.BroadcastChannel import BroadcastChannel

from matplotlib import pyplot as plt
import time


def main():

    topo = Topology()

    graph = nx.Graph()

    graph.add_node(0)
    graph.add_node(1)
    graph.add_node(2)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)

    # nx.draw(graph, with_labels=True)
    # plt.show()

    topo.construct_from_graph(
        G=graph,
        nodetype=BrachaTouegCrashConsensusAlgorithmComponentModel,
        channeltype=BroadcastChannel,
    )

    topo.start()

    time.sleep(1000)
    topo.exit()


if __name__ == "__main__":
    main()
