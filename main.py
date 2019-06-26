from schelling import SchellingModel
import matplotlib.pyplot as plt
import numpy as np

# Random seed setted
np.random.seed(123458)

# Schelling parameters
l = 50 # Linear size of the grid
fraction_pos = 0.50 # Fraction of positive and negative nodes
fraction_neg = 0.20
threshold = 0.80 # Schelling's threshold
neighborhood = 'moore' # Moore's neighborhood: each node has eight neighbors

number_of_iterations = 100 # Evolution steps 

# Create the model
model = SchellingModel(l = l, fraction_pos = fraction_pos, fraction_neg = fraction_neg, threshold = threshold, neighborhood = neighborhood)

# See how many states are in the system
print model.number_of_states()

# Activate the matplotlib interactive mode
#plt.ion()
fig = plt.figure(figsize = (5,5))

# Show the system
#model.image(fig)

# Do 20 iterations, while showing the system
for step in range(number_of_iterations):
	#model.image(fig)
        # Save the final configuration
        model.image(fig, file2save = 'Conf{}.jpg'.format(step))
	model.evolve()

	# Compute in each the mean utility, the number of unsatisfied nodes and the surface length
	print 'Step: {} - Mean utility: {} - Unsatisfied: {} - Surface: {}'.format(step, model.mean_utility(), model.unsatisfied_nodes(), model.surface_length())

# Deactivate interactive matplotlib mode
#plt.ioff()

# Save the final configuration
#model.image(fig, file2save = 'Final_conf.png')
