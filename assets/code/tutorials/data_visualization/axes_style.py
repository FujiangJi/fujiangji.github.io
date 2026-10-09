"""
2.1 set axes parameters
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

fig,ax = plt.subplots(figsize=(6,2), dpi=100)

# x-axis, y-axis label.
ax.set_xlabel('x', fontsize=10, fontweight = 'bold', fontstyle='italic', labelpad = 0.5)
ax.set_ylabel('y', fontsize=10, fontweight = 'bold', fontstyle='italic', labelpad = 0.5)


# tick parameters setting.
"""
ax.tick_params(axis='both', **kwargs)
The parameters include: 
  (1) axis: {'x', 'y', 'both'}, default: 'both'. The axis to which the parameters are applied.
  (2) which: {'major', 'minor', 'both'}, default: 'major'. The group of ticks to which the parameters are applied.
  (3) direction: {'in', 'out', 'inout'}. Puts ticks inside the Axes, outside the Axes, or both.
  (4) length: float. Tick length in points.
  (5) width: float. Tick width in points.
  (6) color: Tick color.
  (7) pad: float. Distance in points between tick and label.
  (8) labelsize: float or str. Tick label font size in points or as a string (e.g., 'large').
  (9) labelcolor: Tick label color.
  (10) colors: Tick color and label color.
  (11) zorder: float. Tick and label zorder.
  (12) bottom, top, left, right: bool. Whether to draw the respective ticks.
  (13) labelbottom, labeltop, labelleft, labelright: bool. Whether to draw the respective tick labels.
  (14) labelrotation: float. Tick label rotation
"""
# Examples
ax.tick_params(labelsize=8)
ax.tick_params(axis = 'x',labelsize=8)
ax.tick_params(axis='both', which='major', direction='in', length=4, width=2,
               color='red', pad = 0.1, labelsize=10, labelrotation=45, labelcolor = "blue", 
               bottom = True, top = False, left = True, right = False,
               labelbottom = True, labeltop = False, labelleft = True, labelright = False)

# set the visiblity of axis
ax.spines[['top', 'right']].set_visible(False)
ax.spines[['bottom','left']].set_linewidth(2)


# set xlim and ylim and display the same number of decimal places.
ax.set_xlim(0,10)
ax.set_ylim(0,10)
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))

# set the facecolor and grid.
ax.set_facecolor((0,0,0,0.03))
ax.grid(color='gray', linestyle=':', linewidth=0.3)
              