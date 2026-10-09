"""
1.1 plt.subplots
 fig,ax = plt.subplots(nrows, ncols, figsize=(width, height), dpi, sharex=False, sharey=False, **kwargs)
 Parameters:
------------------------------
  - fig: figure
  - ax: axes or array of Axes.
  - dpi: the resolution of figure.
  - nrows/ncols: number of rows/columns of the subplot grid.
  - sharex/sharey: bool, default: False.
                   Controls sharing of properties among x (sharex) or y (sharey) axes:
  - figsize: the size of the created figure (Width, height) in inches (float, float).
  - **kwargs: other parameters such as squeeze, width_ratios, height_ratios, subplot_kw, 
              gridspec_kw, etc. that are passed to the pyplot.figure call
"""

import matplotlib.pyplot as plt
# generate a single axes figure (output 1).
fig, ax = plt.subplots(1,1, figsize=(2, 2), dpi=100)
# generate a two rows and two columns axes fugure (output 2). 
# ax[0] (1st row, 1st coloumn), ax[1] (1st row, 2nd coloumn) (1st row, 1st coloumn), ax[2], ax[3] represent each axes.
fig, ax = plt.subplots(2,2, figsize=(3, 3), dpi=100)
# initialize the axes.
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace = 0.1,hspace = 0.1)
plt.rcParams.update(config)

# generate a two rows and two columns axes fugure. 
# ax1 (1st row, 1st coloumn), ax2 (1st row, 2nd coloumn) (1st row, 1st coloumn), ax3, ax4 represent each axes.
fig, ([ax1,ax2],[ax3,ax4]) = plt.subplots(2,2, figsize=(3, 3), dpi=100)
# all the ases share the same x and y label (output 3).
fig.text(0.5, 0, 'x', ha='center')
fig.text(0, 0.5, 'y', va='center',rotation='vertical')