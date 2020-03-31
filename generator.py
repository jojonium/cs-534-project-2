import numpy as np
import random
import matplotlib.pyplot as plt

"""
Generates 4 gaussians, each with 1000 points and a stdev of 1 in each direction.
"""

means = [
    (5, 6),
    (5, 4),
    (6, 5),
    (4, 5)
]
clustersPerPoint = 1000
stdev = 0.75

points = []

colors = []
xs = []
ys = []

for m in means:
    col = (random.random(), random.random(), random.random(), 1)
    for i in range(clustersPerPoint):
        x, y = np.random.normal(m, stdev)
        xs.append(x)
        ys.append(y)
        colors.append(col)
        points.append((x, y))

# make graph
plt.scatter(xs, ys, c=colors)
fig = plt.gcf()
ax = fig.gca()

for i, c in enumerate(means):
    # TODO radius of circle hard-coded, probably a better way to calculate
    center_circle = plt.Circle((c[0], c[1]), 0.01, color="black")
    cluster_circle = plt.Circle((c[0], c[1]), stdev, fill=False, edgecolor="black")
    ax.add_artist(center_circle)
    ax.add_artist(cluster_circle)

plt.show()

for p in points:
    print("{0}, {1}".format(p[0], p[1]))

