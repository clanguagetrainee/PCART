from sklearn import linear_model
reg = linear_model.LassoLars(1.0, precompute='auto', fit_intercept=True, verbose=False, normalize=True, jitter=None, random_state=None)