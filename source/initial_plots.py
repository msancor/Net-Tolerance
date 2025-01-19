#Here we import the packages we will use
import matplotlib.pyplot as plt
from modules.random import RandomNetwork
from modules.scale_free import ScaleFreeNetwork
import networkx as nx

#Here we set the style of the plots
plt.rc('axes', labelsize=12)
plt.rc('axes', titlesize=12)
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rc('legend', fontsize=12)
plt.rc('figure', titlesize=12)
plt.rc('font', family='serif')

if __name__ == '__main__':
    #Here we create a random network and a scale-free network with similar parameters
    N = 130
    AVG_K = 3.3
    p = AVG_K/(N-1)
    rand = RandomNetwork(N, p)
    scale_free = ScaleFreeNetwork(N, AVG_K)

    #Here we plot side by side both networks
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    rand.plot(axs[0])
    scale_free.plot(axs[1])
    #We add a title to the plots
    axs[0].set_title('Random Network')
    axs[1].set_title('Scale-Free Network')

    #Here we save the plot
    plt.tight_layout()
    plt.savefig('figures/initial_plots.png', dpi=300)

    #Now we plot the degree distribution of both networks with a higher number of nodes
    N = 10000
    AVG_K = 3.3
    p = AVG_K/(N-1)
    rand = RandomNetwork(N, p)
    scale_free = ScaleFreeNetwork(N, AVG_K)
    #Here we plot the degree distribution of the random network
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    rand.plot_degree_distribution(axs[0])
    scale_free.plot_degree_distribution(axs[1])
    #We add a title to the plots
    axs[0].set_title('Random Network')
    axs[1].set_title('Scale-Free Network')
    
    #Here we save the plot
    plt.tight_layout()
    plt.savefig('figures/degree_distribution.png', dpi=300)
