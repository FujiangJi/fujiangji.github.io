"""
1.2 plt.figure
 fig = plt.figure(figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True, **kwargs)
 Parameters:
------------------------------
  - fig: figure
  - dpi: the resolution of figure.
  - figsize: the size of the created figure (Width, height) in inches (float, float).
  - dpi:the resolution of the figure in dots-per-inch.
  - facecolorcolor: the background color.
  - edgecolorcolor: the border color.
  - frameonbool, default: True. If False, suppress drawing the figure frame.
  - **kwargs: additional keyword arguments are passed to the Figure constructor.
------------------------------
  Useful for iteratively figure plotting.
"""

import matplotlib.pyplot as plt
# plot a 2*2 axes figure with 100 dpi (output 1).
fig = plt.figure(figsize=(3,3), dpi=100)
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.4,hspace =0.3)
plt.rcParams.update(config)
for i in range(4):
    ax = fig.add_subplot(2,2,i+1)

# plot a 2*2 axes figure with 100 dpi, yellow face and edgecolor (output 2).
fig = plt.figure(figsize=(3,3), dpi=100, facecolor="y", edgecolor="y")
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.4,hspace =0.3)
plt.rcParams.update(config)
for i in range(4):
    ax = fig.add_subplot(2,2,i+1)