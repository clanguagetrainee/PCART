from sklearn import linear_model
clf = linear_model.Lasso(alpha=1.0, fit_intercept=True, normalize=False, random_state=None, selection='cyclic')