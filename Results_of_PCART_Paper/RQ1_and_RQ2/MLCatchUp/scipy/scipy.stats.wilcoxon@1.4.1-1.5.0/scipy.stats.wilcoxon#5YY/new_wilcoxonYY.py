from scipy.stats import wilcoxon
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 10]
result = wilcoxon(x=x, y=y, mode='auto')