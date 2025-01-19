from modules.scale_free import ScaleFreeNetwork
from modules.random import RandomNetwork
from collections import Counter
import matplotlib.pyplot as plt
from typing import Dict, List
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

def get_component_sizes(G:nx.Graph)->List[int]:
    """
    This method will return the sizes of all the components in the network.
    Args:
        G: nx.Graph, the network
    Returns:
        List[int]: the sizes of all the components
    """
    #We get the connected components
    components = list(nx.connected_components(G))
    #We obtain all the sizes
    sizes = [len(component) for component in components]

    return sizes

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

def run_component_sizes_experiment(N:int, AVG_K:int, targeted:bool, random_net:bool = True, iterations:int=50)->List[Dict[int, int]]:
    """
    This method will run the component experiment.
    Args:
        N: int, the number of nodes in the network
        AVG_K: int, the average degree of the network
        targeted: bool, whether to use targeted removal or not
        random_net: bool, whether to create a random network or a scale-free network
        iterations: int, the number of iterations to run
    Returns:
        List[Dict[int, int]]: the sizes of the components for each fraction of nodes removed
    """

    #We create a list to store the sizes
    size= []
    #We create a list with the fractions of nodes to remove
    fractions = [0.05, 0.18, 0.45]
    #We remove the nodes and calculate the sizes
    for fraction in tqdm(fractions):
        temp_results = []
        for _ in range(iterations):
            #We create the network
            net = get_network(N, AVG_K, random_net)
            if targeted:
                G_pruned = targeted_removal(net, fraction)
            else:
                G_pruned = random_removal(net, fraction)

            #We get the sizes
            temp_results.extend(get_component_sizes(G_pruned))
        size.append(Counter(temp_results))

    return size

#Here we start the main program
if __name__ == "__main__":
    #We make 6 plots all for scale-free networks, 3 for random removal and 3 for targeted removal
    #We plot the component size distribution for 3 different fractions of nodes removed
    N = 10000
    AVG_K = 4

    #We run the experiment
    results_random = run_component_sizes_experiment(N, AVG_K, False, False)
    results_targeted = run_component_sizes_experiment(N, AVG_K, True, False)

    #We plot the results all in log-log scale
    fig, ax = plt.subplots(2, 3, figsize=(15, 10), sharey=True, sharex=True)
    for i in range(3):
        #We plot the results for random removal
        sizes = list(results_random[i].keys())
        counts = list(results_random[i].values())
        #We normalize the counts
        counts = [count/sum(counts) for count in counts]
        ax[1, i].scatter(sizes, counts, color='blue', marker='o', facecolors='none')
        ax[1, i].set_xscale('log')
        ax[1, i].set_yscale('log')
        #We mantain the ticks in both axis
        ax[1,i].xaxis.set_tick_params(which='both', labelbottom=True)
        ax[1,i].yaxis.set_tick_params(which='both', labelleft=True)

        
        #We plot the results for targeted removal
        sizes = list(results_targeted[i].keys())
        counts = list(results_targeted[i].values())
        #We normalize the counts
        counts = [count/sum(counts) for count in counts]
        ax[0, i].scatter(sizes, counts, color='red', marker='o', facecolors='none')
        ax[0, i].set_xscale('log')
        ax[0, i].set_yscale('log')
        #We mantain the ticks in both axis
        ax[0,i].xaxis.set_tick_params(which='both', labelbottom=True)
        ax[0,i].yaxis.set_tick_params(which='both', labelleft=True)

    ax[1, 0].set_ylabel('Random removal')
    ax[0, 0].set_ylabel('Targeted removal')
    ax[1, 0].set_xlabel('f=0.05')
    ax[1, 1].set_xlabel('f=0.18')
    ax[1, 2].set_xlabel('f=0.45')

    #Here we save the plot
    plt.tight_layout()
    plt.savefig('figures/component_sizes.png', dpi=300)
    