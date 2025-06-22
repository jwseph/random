import numpy as np
import matplotlib.pyplot as plt

pts = {
    'gen ed': (2, 2, 2),
    'AP': (5, 5, 5),
    'UW': (3, 8, 6),
    'math comp': (16, 3, 5),
    'MIT': (12, 15, 19),
    'coursera': (3, 10, 4),
    'good books': (7, 18, 4),
}

x, y, z = map(np.array, zip(*pts.values()))

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_xbound(0, 20)
ax.set_ybound(0, 20)
ax.set_zbound(0, 20)
ax.set_xlabel('critical thinking')
ax.set_ylabel('usefulness/interestingness')
ax.set_zlabel('work/effort required')
ax.set_title('class quality comparison (hard sciences/mostly CS)')

cmap = plt.get_cmap('plasma')
colors = cmap(np.interp(y/z, (min(y/z), max(y/z)), (0.05, 0.9)))
ax.scatter(x, y, z, s=100, c=colors, marker='o')
for label, (x, y, z) in pts.items():
    ax.text(x, y, z, label, fontsize=9, ha='right', va='bottom')
    
plt.show()