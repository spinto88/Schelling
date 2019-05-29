from schelling import SchellingModel
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(123457)

model = SchellingModel(l = 50, fraction_pos = 0.20, fraction_neg = 0.00, threshold = 4.00/8, neighborhood = 'moore')

fig = plt.figure()

#model.image(fig, file2save = 'Conf1.png')

plt.ion()

model.image(fig)
for i in range(100):
    model.evolve()
    model.image(fig)
    print 'Iteration number {}'.format(i)

plt.ioff()

model.image(fig)
