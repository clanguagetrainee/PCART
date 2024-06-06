from sklearn.decomposition import dict_learning_online
import numpy as np
X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
dict_learning_online(iter_offset=0, n_components=2, X=X, max_iter=None, tol=0.001, max_no_improvement=10)