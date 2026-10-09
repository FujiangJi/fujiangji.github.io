# common settings
ax.legend(loc='upper right',fontsize=12, facecolor= 'none',edgecolor = 'none',bbox_to_anchor=(2.0, 0.7), ncol = 2, columnspacing = 0.4)
# remove legend
ax.legend_.remove()
# sometimes we need to re-define the legend as the alpha or other parameter settings in the figure.
handles, labels = ax.get_legend_handles_labels()
k = 0
new_handles = []
for handle in handles:
    new_handle = plt.Line2D([], [], ls = "none", marker='o', color = original_handle_colors[k], markersize = 8, alpha = 1)
    new_handles.append(new_handle)
    k = k+1
legend = ax.legend(handles=new_handles, labels=labels,loc = 'lower right',fontsize=8.5, facecolor= 'none',edgecolor = 'none',bbox_to_anchor=(1.,0))