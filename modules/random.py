"""
Here we create a class that will generate a random network using the Erdös-Rényi model.
"""
#First we import the necessary libraries
import matplotlib.pyplot as plt
from collections import Counter
from typing import List
import networkx as nx
import numpy as np
import math

class RandomNetwork:
    """
    This class will generate a random network using the Erdös-Rényi model.
    """
    def __init__(self, n:int, p:float)->None:
        """
        The constructor will create a random network with n nodes and probability p of connecting two nodes.
        Args:
            n: int, the number of nodes in the network.
            p: float, the probability of connecting two nodes
        Returns:
            None
        """
        self.n = n
        self.p = p
        self.G = nx.fast_gnp_random_graph(self.n, self.p)

    def get_hubs(self, top_k:int)->List[int]:
        """
        This method will return the top-k nodes with higher degree.
        Args:
            top_k: int, the number of nodes to return
        Returns:
            List[int]: the top-k nodes with higher degree
        """
        #We get the degree of each node
        degree = dict(self.G.degree())
        #We sort the nodes by degree
        sorted_degree = {k: v for k, v in sorted(degree.items(), key=lambda item: item[1], reverse=True)}
        #We get the top-k nodes
        top_k_nodes = list(sorted_degree.keys())[:top_k]

        return top_k_nodes
        
    def plot(self, ax:plt.Axes)->None:
        """
        This method will plot the random network.
        We will color with red the top-5 nodes with higher degree and in green their neighbors. Every other node will be colored in blue.
        #We draw using the Kamada-Kawai layout

        Args:
            ax: plt.Axes, the axes where to plot the network
        Returns:
            None
        """
        #We get the top-5 nodes with higher degree
        top_5 = self.get_hubs(5)
        #We get the neighbors of the top-5 nodes
        neighbors = []
        for node in top_5:
            neighbors.extend(list(self.G.neighbors(node)))

        #We create a color map for the nodes
        color_map = []
        for node in self.G:
            if node in top_5:
                color_map.append('red')
            elif node in neighbors:
                color_map.append('green')
            else:
                color_map.append('darkblue')

        #We draw the network
        pos = nx.kamada_kawai_layout(self.G)
        nx.draw(self.G, pos, node_color=color_map, with_labels=False, node_size=50, edge_color='gray', linewidths=0.5, ax=ax)

        return None
    
    def plot_degree_distribution(self, ax:plt.Axes)->None:
        """
        This method will plot the degree distribution of the random network.
        It also plots a Poisson distribution with the same average degree.
        Args:
            ax: plt.Axes, the axes where to plot the degree distribution
        Returns:
            None
        """
        #We plot the degree distribution
        #First we get the degrees of the nodes
        degrees = [degree for node, degree in self.G.degree()]
        #Now we count the number of nodes with each degree and normalize it
        degree_distribution = Counter(degrees)
        degree_distribution = {degree: count/self.n for degree, count in degree_distribution.items()}
        #We plot the degree distribution
        ax.bar(degree_distribution.keys(), degree_distribution.values(), color='darkblue', label='Degree Distribution')

        #We plot the Poisson distribution as a line
        average_degree = self.average_degree()
        x = np.arange(0, max(degrees)+1)
        poisson = np.exp(-average_degree)*np.power(average_degree, x)/np.array([math.factorial(i) for i in x])
        ax.plot(x, poisson, color='red', label='Poisson Distribution')

        ax.set_xlabel('Degree')
        ax.set_ylabel('Density')
        ax.legend()

        return None

        
    def average_degree(self)->float:
        """
        This method will return the average degree of the network.
        """
        return np.mean(list(dict(self.G.degree()).values()))
    
    def clustering_coefficient(self)->float:
        """
        This method will return the clustering coefficient of the network.
        """
        return nx.average_clustering(self.G)
    