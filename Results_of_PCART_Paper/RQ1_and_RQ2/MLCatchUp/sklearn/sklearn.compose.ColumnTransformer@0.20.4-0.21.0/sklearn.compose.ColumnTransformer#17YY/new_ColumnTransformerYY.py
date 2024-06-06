import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import Normalizer
ct = ColumnTransformer([('norm1', Normalizer(norm='l1'), [0, 1]), ('norm2', Normalizer(norm='l1'), slice(2, 4))], 'drop', 0.3, n_jobs=None, transformer_weights=None, verbose=False)