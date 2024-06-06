from scipy.stats import circmean
samples = [0.1, 0.2, 6.0, 6.1]
result = circmean(samples, high=6.283185307179586, nan_policy='propagate')
print(result)