"""
1.3 plt.figure & GridSpec
 gs = gridspec.GridSpec(nrows, ncols)
 A grid layout to place subplots within a figure.
Parameters:
------------------------------
  - nrows/ncols: the number of rows and columns of the grid (int).
  - other parameters: https://matplotlib.org/stable/api/_as_gen/matplotlib.gridspec.GridSpec.html
  - detailed tutorial: https://matplotlib.org/3.5.0/tutorials/intermediate/gridspec.html
------------------------------
  Useful for plotting irregular axes.
  Useful for iteratively figure plotting.

"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
# plot a 1*4 axes figure with 100 dpi using GridSpec
fig = plt.figure(figsize=(8,2), dpi=100)
gs = gridspec.GridSpec(2, 8)
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.7,hspace =0.1)
plt.rcParams.update(config)
# can also use interative loop to generate axes.
ax1 = plt.subplot(gs[0:2, 0:2])
ax2 = plt.subplot(gs[0:2, 2:4])
ax3 = plt.subplot(gs[0:2, 4:6])
ax4 = plt.subplot(gs[0:2, 6:8])