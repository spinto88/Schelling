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

    def potential_utility(self, node, potential_state):

        same_state = [1 if self.node[neighbour]['state'] == potential_state else 0 for neighbour in self.neighbors(node)]

        return np.float(np.sum(same_state)) / self.degree(node)

    def mean_utility(self):

        return np.mean([self.utility(node) for node in self.occupied_nodes])

    def unsatisfied_nodes(self):
            
        unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
        return len(unsatisfied_nodes)

    def surface_length(self):

        surface = 0
        for node in self.nodes():
            for neighbour in self.neighbors(node):
                if self.node[node]['state'] != self.node[neighbour]['state']:
                    surface += 1

        return int(surface * 0.5)

    def evolve(self):

        changes = 0
            
#        np.random.shuffle(self.occupied_nodes)
        unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
        np.random.shuffle(unsatisfied_nodes)

        """
        unsatisfied_nodes = []
        for node in self.occupied_nodes:
            if self.utility(node) < self.threshold:
                 unsatisfied_nodes.append(node)
                 if len(unsatisfied_nodes) >= 100:
                     break
        """
        if len(unsatisfied_nodes) == 0:
            print 'There is no unsatisfied nodes'
            return None

        for random_unsatisfied_node in unsatisfied_nodes:

            if self.utility(random_unsatisfied_node) < self.threshold:

                random_free_node = self.free_nodes[np.random.choice(range(len(self.free_nodes)))]
 
                self.node[random_free_node]['state'] = self.node[random_unsatisfied_node]['state']

                self.occupied_nodes.remove(random_unsatisfied_node)
                self.occupied_nodes.append(random_free_node)

    	        self.node[random_unsatisfied_node]['state'] = 0

                self.free_nodes.remove(random_free_node)
                self.free_nodes.append(random_unsatisfied_node)

                changes += 1
            else:
                pass

        return changes

    def unsatisfied_nodes(self):
            
        unsatisfied_nodes = [node for node in self.occupied_nodes if self.utility(node) < self.threshold]
        return len(unsatisfied_nodes)

    def image(self, fig, file2save = None):

        import matplotlib.pyplot as plt

        color_dict = {-1: (0.90, 0.00, 0.00, 0.75), 1: (0.00, 0.00, 0.90, 0.75), 0: (0.30, 0.90, 0.30, 0.30)}

        matrix2show = np.zeros([self.l, self.l, 4])

        for node in self.nodes:
           matrix2show[node] = color_dict[self.node[node]['state']]

        fig.clf()
        ax = fig.add_subplot(1,1,1)
        ax.imshow(matrix2show)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('Unsatisfied nodes {} - Surface {}'.format(self.unsatisfied_nodes(), \
								self.surface_length()))
        fig.canvas.draw()

        if file2save is not None:
            fig.set_size_inches(13, 13)
            fig.savefig(file2save, dpi = 300)
        else:
            plt.show()
