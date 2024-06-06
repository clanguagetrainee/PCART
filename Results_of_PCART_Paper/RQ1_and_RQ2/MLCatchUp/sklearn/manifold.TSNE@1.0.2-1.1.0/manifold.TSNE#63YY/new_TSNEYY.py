import numpy as np
from sklearn.manifold import TSNE
X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
X_embedded = TSNE(min_grad_norm=1e-07, n_components=2).fit_transform(X, metric_params=None)