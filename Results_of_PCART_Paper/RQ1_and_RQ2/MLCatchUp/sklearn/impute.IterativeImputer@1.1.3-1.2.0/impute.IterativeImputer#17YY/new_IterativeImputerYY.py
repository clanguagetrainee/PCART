import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
imp_mean = IterativeImputer(sample_posterior=False, tol=0.001, missing_values=0, max_iter=10, keep_empty_features=False)