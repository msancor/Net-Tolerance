"""
Here we create a class that will generate a scale-free network using the Barabási-Albert model.
"""
#First we import the necessary libraries
import matplotlib.pyplot as plt
from collections import Counter
from typing import List
import powerlaw as pwl
import networkx as nx
import numpy as np


class ScaleFreeNetwork:
    """
    This class will generate a random network using the Erdös-Rényi model.
    """
    def __init__(self, n:int, avg_degree:float=4)->None:
        """
        The constructor will create a scale free network with n nodes and average degree avg_degree.
        Args:
            n: int, the number of nodes in the network.
            avg_degree: float, the average degree of the network
        Returns:
            None
        """
        self.n = n
        self.avg_degree = avg_degree
        self.m = int(avg_degree/2)
        self.G = nx.barabasi_albert_graph(self.n, self.m)
        
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
        This method will plot the degree distribution of the scale-free network.
        It also fits a line to the degree distribution in log-log scale.
        Args:
            ax: plt.Axes, the axes where to plot the degree distribution
        Returns:
            None
        """
        #We plot the degree distribution in log-log scale and fitting a line
        #First we get the degrees of the nodes
        deg=dict(self.G.degree()).values()
        deg_distri=Counter(deg)
        degree = list(deg)
        #We plot the normalized degree distribution
        normalized_degree = [x/self.n for x in list(deg_distri.values())]
        ax.scatter(deg_distri.keys(), normalized_degree, label='Degree distribution', color='darkblue')
        #We fit a line to the degree distribution
        fit = pwl.Fit(degree, discrete=True, xmin=1, xmax=45)
        fit.power_law.plot_pdf(color='r', linestyle='--', ax=ax, label=f'Power law fit\nalpha={fit.power_law.alpha:.2f}')
        ax.set_xscale('log')
        ax.set_yscale('log')
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
    