import matplotlib.pyplot as plt
x = [45, 25, 15, 15]
plt.pie(x, None, ['A', 'B', 'C', 'D'], None, autopct='%1.1f%%', pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=90, radius=1, counterclock=True, wedgeprops=None, textprops=None, center=(0, 0), frame=False, hatch=None)