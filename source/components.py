from modules.scale_free import ScaleFreeNetwork
from modules.random import RandomNetwork
import matplotlib.pyplot as plt
from typing import List, Tuple
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

def get_component_sizes(G:nx.Graph)->Tuple[float]:
    """
    This method will return the size of the largest component and the average size of the other components.
    Args:
        G: nx.Graph, the network
    Returns:
        Tuple[float]: the size of the largest component and the average size of the other components
    """
    #We get the connected components
    components = list(nx.connected_components(G))
    #We sort the components by size
    sorted_components = sorted(components, key=len, reverse=True)
    #We get the size of the largest component
    largest_component = len(sorted_components[0])/G.number_of_nodes() if len(sorted_components) > 0 else 0
    #We get the size of the other components
    other_components = [len(component) for component in sorted_components[1:]]
    #We get the average size of the other components
    avg_other_components = np.mean(other_components)

    return largest_component, avg_other_components

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

def run_component_experiment(N:int, AVG_K:int, targeted:bool, random_net:bool = True, iterations:int=50)->List[Tuple[float]]:
    """
    This method will run the component experiment.
    Args:
        N: int, the number of nodes in the network
        AVG_K: int, the average degree of the network
        targeted: bool, whether to use targeted removal or not
        random_net: bool, whether to create a random network or a scale-free network
        iterations: int, the number of iterations to run
    Returns:
        List[Tuple[float]:]: the size of the largest component and the average size of the other components
    """

    #We create a list to store the sizes
    relative_size, avg_size = [], []
    #We create a list with the fractions of nodes to remove
    fractions = np.linspace(0, 1, 30)
    #We remove the nodes and calculate the sizes
    for fraction in tqdm(fractions):
        temp_results_relative_size, temp_results_avg_size = [], []
        for _ in range(iterations):
            #We create the network
            net = get_network(N, AVG_K, random_net)
            if targeted:
                G_pruned = targeted_removal(net, fraction)
            else:
                G_pruned = random_removal(net, fraction)

            #We get the sizes
            largest_component, avg_other_components = get_component_sizes(G_pruned)
            temp_results_relative_size.append(largest_component)
            temp_results_avg_size.append(avg_other_components)
        
        relative_size.append(np.mean(temp_results_relative_size))
        avg_size.append(np.mean(temp_results_avg_size))

    return relative_size, avg_size

#Here we start the main program
if __name__ == "__main__":
    #We plot the results both for the random and targeted removal
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    relative_size_random_er, avg_size_random_er = run_component_experiment(10000, 4, False)
    relative_size_random_ba, avg_size_random_ba = run_component_experiment(10000, 4, False, False)
    relative_size_targeted_er, avg_size_targeted_er = run_component_experiment(10000, 4, True)
    relative_size_targeted_ba, avg_size_targeted_ba = run_component_experiment(10000, 4, True, False)

    #First we plot for the ER network
    
    ax[0].scatter(np.linspace(0, 1, 30), relative_size_random_er, label="S Failure", color="darkblue", marker="s", facecolors="none")
    ax[0].scatter(np.linspace(0, 1, 30), avg_size_random_er, label="<s> Failure", color="darkblue", marker="s")
    ax[0].scatter(np.linspace(0, 1, 30), relative_size_targeted_er, label="S Attack", color="red", marker="o", facecolors="none")
    ax[0].scatter(np.linspace(0, 1, 30), avg_size_targeted_er, label="<s> Attack", color="red", marker="o")
    #We add Erdős-Rényi network as title
    ax[0].set_title("Erdős-Rényi network")
    #We set the axis labels
    ax[0].set_xlabel("f")
    ax[0].set_ylabel("<s> and S")
    #Add the legend
    ax[0].legend()
    
    #We plot for the BA network
    ax[1].scatter(np.linspace(0, 1, 30), relative_size_random_ba, label="S Failure", color="darkblue", marker="s", facecolors="none")
    ax[1].scatter(np.linspace(0, 1, 30), avg_size_random_ba, label="<s> Failure", color="darkblue", marker="s")
    ax[1].scatter(np.linspace(0, 1, 30), relative_size_targeted_ba, label="S Attack", color="red", marker="o", facecolors="none")
    ax[1].scatter(np.linspace(0, 1, 30), avg_size_targeted_ba, label="<s> Attack", color="red", marker="o")
    #We add Barabási-Albert network as title
    ax[1].set_title("Barabási-Albert network")
    #We set the axis labels
    ax[1].set_xlabel("f")
    ax[1].set_ylabel("<s> and S")
    #Add the legend
    ax[1].legend()
    #We save the figure
    plt.tight_layout()
    plt.savefig("figures/component_robustness.png", dpi=300)