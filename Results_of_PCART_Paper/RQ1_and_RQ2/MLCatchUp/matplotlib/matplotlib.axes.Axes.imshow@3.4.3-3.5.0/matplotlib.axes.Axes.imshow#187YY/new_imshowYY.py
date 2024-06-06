import matplotlib.pyplot as plt
import numpy as np
X = np.random.rand(100, 100)
plt.imshow(X, filternorm=True, filterrad=4.0, aspect='auto', cmap='viridis', interpolation='nearest', norm=None, interpolation_stage=None)