from schelling import SchellingModel

model = SchellingModel(l = 50, fraction_pos = 0.30, fraction_neg = 0.30, threshold = 0.50, neighborhood = 'moore')

for i in range(10):
    model.evolve(100)
    print model.mean_utility()

#model.evol2convergence()

model.image()
