import matplotlib.pyplot as plt
x = [45, 25, 15, 15]
plt.pie(x, None, ['A', 'B', 'C', 'D'], None, '%1.1f%%', 0.6, labeldistance=1.1, shadow=False, counterclock=True, radius=1, normalize=True, data=None, startangle=90, hatch=None)