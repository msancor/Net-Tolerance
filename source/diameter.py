
from modules.scale_free import ScaleFreeNetwork
from modules.random import RandomNetwork
import matplotlib.pyplot as plt
from typing import List
from tqdm import tqdm
import networkx as nx
import numpy as np

#Here we set the style of the plots
plt.rc('axes', labelsize=12)
plt.rc('axes', titlesize=12)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=12)
plt.rc('font', family='serif')


def random_removal(G:nx.Graph, fraction:float)->nx.Graph:
        """
        This method will remove a fraction of nodes randomly from the network.
        Args:
            G: nx.Graph, the network from which to remove the nodes
            fraction: float, the fraction of nodes to remove
        Returns:
            nx.Graph: the network with the nodes removed
        """
        #We get a list of the node labels
        nodes = list(G.nodes())
        #We shuffle the list
        np.random.shuffle(nodes)
        #We remove the nodes
        nodes_to_remove = nodes[:int(fraction*G.number_of_nodes())]
        G.remove_nodes_from(nodes_to_remove)

        return G

    
def targeted_removal(G:nx.Graph, fraction:float)->nx.Graph:
    """
    This method will remove a fraction of nodes using the targeted removal strategy.
    Args:
        G: nx.Graph, the network from which to remove the nodes
        fraction: float, the fraction of nodes to remove
    Returns:
        nx.Graph: the network with the nodes removed
    """
    #We get the nodes to remove
    nodes_to_remove = get_hubs(G, int(fraction*G.number_of_nodes()))
    #We remove the nodes
    G.remove_nodes_from(nodes_to_remove)

    return G

def get_hubs(G:nx.Graph, top_k:int)->List[int]:
    """
    This method will return the top-k nodes with higher degree.
    Args:
        top_k: int, the number of nodes to return
    Returns:
        List[int]: the top-k nodes with higher degree
    """
    #We get the degree of each node
    degree = dict(G.degree())
    #We sort the nodes by degree
    sorted_degree = {k: v for k, v in sorted(degree.items(), key=lambda item: item[1], reverse=True)}
    #We get the top-k nodes
    top_k_nodes = list(sorted_degree.keys())[:top_k]

    return top_k_nodes

def get_largest_component(G:nx.Graph)->nx.Graph:
    """
    This method will return the induced subgraph of the largest connected component.
    Args:
        G: nx.Graph, the network to get the largest component
    Returns:
        nx.Graph: the induced subgraph of the largest connected component
    """
    if nx.number_connected_components(G) >= 1:
        largest_component = max(nx.connected_components(G), key=len)
        return G.subgraph(largest_component)
    else:
         return G

def diameter(G:nx.Graph)->int:
        """
        This method will return the diameter of the network.
        Args:
            G: nx.Graph, the network to calculate the diameter
        Returns:
            int: the diameter of the network
        """
        if nx.number_connected_components(G) == 0:
            return 0
        return nx.algorithms.approximation.diameter(G)

def get_network(N:int, AVG_K:int, random_net:bool = True)->nx.Graph:
    """
    This method will return a network of N nodes with average degree AVG_K.
    Args:
        N: int, the number of nodes in the network
        AVG_K: int, the average degree of the network
        random_net: bool, whether to create a random network or a scale-free network
    Returns:
        nx.Graph: the network
    """
    if random_net:
        p = AVG_K/(N-1)
        return RandomNetwork(N, p).G
    else:
        return ScaleFreeNetwork(N, AVG_K).G

def run_diameter_robustness_experiment(N:int, AVG_K:int, targeted:bool, random_net:bool = True, iterations:int=50)->List[float]:
    """
    This method will run the diameter robustness experiment.
    Args:
        N: int, the number of nodes in the network
        AVG_K: int, the average degree of the network
        targeted: bool, whether to use targeted removal or not
        random_net: bool, whether to create a random network or a scale-free network
        iterations: int, the number of iterations to run
    Returns:
        List[float]: the diameters of the network as a function of the fraction of nodes removed
    """

    #We create a list to store the diameters
    diameters = []
    #We create a list with the fractions of nodes to remove
    fractions = np.linspace(0, 1, 30)
    #We remove the nodes and calculate the diameter
    for fraction in tqdm(fractions):
        temp_results = []
        for _ in range(iterations):
            #We create the network
            net = get_network(N, AVG_K, random_net)
            if targeted:
                G_pruned = targeted_removal(net, fraction)
            else:
                G_pruned = random_removal(net, fraction)

            temp_results.append(diameter(get_largest_component(G_pruned)))
        diameters.append(np.mean(temp_results))
    return diameters

#Here we start the main program
if __name__ == "__main__":
    #We plot the results both for the random and targeted removal
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    diameters_random_er = run_diameter_robustness_experiment(10000, 4, False)
    diameters_random_ba = run_diameter_robustness_experiment(10000, 4, False, False)
    diameters_targeted_er = run_diameter_robustness_experiment(10000, 4, True)
    diameters_targeted_ba = run_diameter_robustness_experiment(10000, 4, True, False)
    ax.scatter(np.linspace(0, 1, 30), diameters_random_er, label="Failure ER", color="darkblue", marker="^", facecolors="none")
    ax.scatter(np.linspace(0, 1, 30), diameters_random_ba, label="Failure BA", color="darkblue", marker="s", facecolors="none")
    ax.scatter(np.linspace(0, 1, 30), diameters_targeted_er, label="Attack ER", color="red", marker="D", facecolors="none")
    ax.scatter(np.linspace(0, 1, 30), diameters_targeted_ba, label="Attack BA", color="red", marker="o", facecolors="none")
    ax.set_xlabel("f")
    ax.set_ylabel("d")
    ax.legend()
    plt.tight_layout()
    plt.savefig("figures/diameter_robustness.png", dpi=300)


