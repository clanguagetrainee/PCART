from sklearn.feature_selection import r_regression
import numpy as np
X = np.array([[1, 2, 3.1], [2.3, 5.4, 4.3]]).T
y = np.array([1, 2, 3.1])
r_regression(X, y=y, center=True, force_finite=True)