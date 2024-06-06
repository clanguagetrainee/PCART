from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV
(X, y) = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=42)
base_clf = GaussianNB()
calibrated_clf = CalibratedClassifierCV(cv=3, base_estimator=base_clf, ensemble=True, method='sigmoid', n_jobs=None, estimator=None)