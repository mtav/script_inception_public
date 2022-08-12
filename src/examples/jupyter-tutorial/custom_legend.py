# https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/custom_legends.html
# sphinx_gallery_thumbnail_number = 2
from matplotlib import rcParams, cycler
import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

N = 10
data = [np.logspace(0, 1, 100) + np.random.randn(100) + ii for ii in range(N)]
data = np.array(data).T
cmap = plt.cm.coolwarm
rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N)))

fig, ax = plt.subplots()
lines = ax.plot(data)
ax.legend([lines[0], lines[-1]], ['a', 'b'])
plt.show()

#from matplotlib.lines import Line2D
#custom_lines = [Line2D([0], [0], color=cmap(0.), lw=4),
                #Line2D([0], [0], color=cmap(.5), lw=4),
                #Line2D([0], [0], color=cmap(1.), lw=4)]

#fig, ax = plt.subplots()
#lines = ax.plot(data)
#ax.legend(custom_lines, ['Cold', 'Medium', 'Hot'])
