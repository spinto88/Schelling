import networkx as nx 
import numpy as np
import warnings

class SchellingModel(nx.Graph):

    def __init__(self, l, fraction_pos, fraction_neg, threshold, neighborhood = 'nearest'):

        self.l = l
        self.n = l**2

        if fraction_pos + fraction_neg >= 1.00:
            warnings.warn('The fraction of empty sites must be greater than 0')
            exit()

        nx.Graph.__init__(self)
        nx.grid_2d_graph(l, l, periodic = True, create_using = self)
        if neighborhood == 'nearest':
            pass
        elif neighborhood == 'moore':
            for node in self.nodes:
                self.add_edge(node, ((node[0] + 1)%l, (node[1] + 1)%l))
                self.add_edge(node, ((node[0] + 1)%l, (node[1] - 1 + l)%l))

        for node in self.nodes:
            self.node[node]['state'] = np.random.choice([1, -1, 0],\
	        p = [fraction_pos, fraction_neg, \
		1.00 - fraction_pos - fraction_neg])

        self.threshold = threshold

        self.occupied_nodes = [node for node in self.nodes if self.node[node]['state'] != 0]
        self.free_nodes = [node for node in self.nodes if self.node[node]['state'] == 0]

    def number_of_states(self):

        pos_nodes = len([node for node in self.nodes if self.node[node]['state'] == 1])
        neg_nodes = len([node for node in self.nodes if self.node[node]['state'] == -1])
        free_nodes = len([node for node in self.nodes if self.node[node]['state'] == 0])

        return {'Pos': pos_nodes, 'Neg': neg_nodes, 'Free': free_nodes}

    def utility(self, node):

        same_state = [1 if self.node[neighbour]['state'] == self.node[node]['state'] else 0 for neighbour in self.neighbors(node)]

        return np.float(np.sum(same_state)) / self.degree(node)

    def mean_utility(self):

        return np.mean([self.utility(node) for node in self.occupied_nodes])

    def potential_utility(self, node, potential_state):

        same_state = [1 if self.node[neighbour]['state'] == potential_state else 0 for neighbour in self.neighbors(node)]

        return np.float(np.sum(same_state)) / self.degree(node)

    def evolve(self, steps):

        accepted_steps = 0

        for step in range(steps):

            unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
            if len(unsatisfied_nodes) == 0:
                break

            random_unsatisfied_node = unsatisfied_nodes[np.random.choice(len(unsatisfied_nodes))]

   	    potential_free_nodes = [node for node in self.free_nodes \
			if self.potential_utility(node, self.node[random_unsatisfied_node]['state']) >= self.threshold]

            if len(potential_free_nodes) != 0:

                random_free_node = potential_free_nodes[np.random.choice(len(potential_free_nodes))]
  
	        self.node[random_free_node]['state'] = self.node[random_unsatisfied_node]['state']

                self.occupied_nodes.remove(random_unsatisfied_node)
                self.occupied_nodes.append(random_free_node)

    	        self.node[random_unsatisfied_node]['state'] = 0

                self.free_nodes.remove(random_free_node)
                self.free_nodes.append(random_unsatisfied_node)

                accepted_steps += 1

        return accepted_steps

    def evol2convergence(self, max_step = 100):

        steps = 0
        unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
        while len(unsatisfied_nodes) != 0 and steps < max_step:
            self.evolve(1000)
            unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
            steps += 1

        return steps*1000

    def unsatisfied_nodes(self):
            
        unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
        return unsatisfied_nodes

    def image(self, file2save = None):

        import matplotlib.pyplot as plt
        plt.figure(figsize = (13,13))

        color_dict = {-1: (0.90, 0.00, 0.00, 0.75), 1: (0.00, 0.00, 0.90, 0.75), 0: (0.50, 0.90, 0.50, 0.25)}

        matrix2show = np.zeros([self.l, self.l, 4])

        for node in self.nodes:
           matrix2show[node] = color_dict[self.node[node]['state']]

        plt.imshow(matrix2show)
        plt.xticks([])
        plt.yticks([])
        plt.grid(True)
        if file2save is not None:
            plt.savefig(file2save, dpi = 300)
        plt.show()
