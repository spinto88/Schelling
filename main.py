from schelling import SchellingModel
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(123457)

model = SchellingModel(l = 60, fraction_pos = 0.3, fraction_neg = 0.2, threshold = 4.00/8, neighborhood = 'moore')

model.image()
#exit()
print model.mean_utility()
for i in range(20):
    model.evolve()
    plt.ion()
    model.image()
#    print model.mean_utility(), model.unsatisfied_nodes(), model.number_of_states()

print model.mean_utility()
#model.evol2convergence()

model.image()
