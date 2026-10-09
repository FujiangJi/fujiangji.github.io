import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# open the dataset.
df_traits = pd.read_csv("data/NEON_AOP_trait_points.csv")
df = df_traits[["Chla+b", "Ccar", "EWT","Nitrogen","PFT"]]

# define the unit of each traits
unit1 = '($\mu g/cm^2$)'
unit2 = '($g/m^2$)'

# define the palettes for each PFT, either self difine differnt color or sns.hls_palette()
palettes = ["deepskyblue", "orangered","magenta", "limegreen", "darkorange", "darkblue", "darkturquoise", "orchid"]
# palettes = sns.hls_palette(len(df["PFT"].unique()))

# use the sns.pairplot() to show the covariance of different variables.
grid = sns.pairplot(df,hue = "PFT",kind='reg',corner=True,palette = palettes,
                    plot_kws={"scatter_kws": {"alpha": 0.1, "s":2},"line_kws":{"alpha": 0.3}},diag_kws={"alpha": 0.5})

grid.fig.patch.set_facecolor('none')  # Make figure background transparent
grid.fig.patch.set_alpha(0)          # Set transparency level for the figure background
for ax in grid.fig.axes:
    ax.set_facecolor('none')         # Make axes background transparent
    
# set the x/y labels.
label = [f"Chla+b {unit1}", f"Ccar {unit1}",  f"EWT {unit2}", f"Nitrogen {unit1}"]
for i in range(1,4):
    grid.axes[i,0].set_ylabel(label[i],fontsize = 12, color = "white")
    grid.axes[i,0].tick_params(labelsize=12, colors = 'white')
    grid.axes[i,0].spines[['bottom', 'left']].set_color('white')
for i in range(0,4):
    grid.axes[3,i].set_xlabel(label[i],fontsize = 12, color = "white")
    grid.axes[3,i].tick_params(labelsize=12, colors = 'white')
    grid.axes[3,i].spines[['bottom', 'left']].set_color('white')
for i in range(0,4):
    grid.axes[i,i].spines[['bottom', 'left']].set_color('white')
    grid.axes[i,i].tick_params(labelsize=12, colors = 'white')
grid.axes[2,1].spines[['bottom', 'left']].set_color('white')
grid.axes[2,1].tick_params(labelsize=12, colors = 'white')

# add text inside the figure.
grid.axes[0,0].text(1.05,0.1, f"Covariance of plant traits across PFTs",transform=grid.axes[0,0].transAxes, 
                    fontsize = 12, color = "white", fontweight = "bold",fontstyle='italic')
grid.axes[0,0].text(1.05,0, f" n = {len(df)}.",transform=grid.axes[0,0].transAxes, fontsize = 12, 
                    color = "white", fontweight = "bold",fontstyle='italic')

# add the pearson value of trait-trait relationships for each PFT.
for i, j in zip(*plt.np.triu_indices_from(grid.axes, 1)):
    r, _ = pearsonr(df.iloc[:, i], df.iloc[:, j])
    grid.axes[j, i].annotate(f"$r$ = {r:.2f} (overall)", (0.02, 0.95), xycoords='axes fraction', fontsize=9, color='white',fontweight = "bold")

    k = 0
    loc = 0
    for pft in df["PFT"].unique():
        temp = df[df["PFT"] == pft]
        r, _ = pearsonr(temp.iloc[:, i], temp.iloc[:, j])
        grid.axes[j, i].annotate(f"$r$ = {r:.2f}", (0.02, 0.8-loc), xycoords='axes fraction', fontsize=9, color=palettes[k],fontweight = "bold")
        k = k+1
        loc = loc+0.08

# add additional information for trait samples.
k = 0
loc = 0
sns.move_legend(grid, "lower center",bbox_to_anchor=(0.76,0.3), title="PFTs", frameon=False, fontsize = 12)
for pft in df["PFT"].unique():
    temp = df[df["PFT"] == pft]
    nums = len(temp)
    grid.axes[1,1].annotate(f"{pft}: n = {nums}", (1.2, 0.7-loc), xycoords='axes fraction',color=palettes[k],fontsize=12,fontstyle='italic')
    k = k+1
    loc = loc+0.1

# set the legend parameters.
grid._legend.set_title("PFTs",prop={'size': 12})
title = grid._legend.get_title()       
title.set_color("white")

for handle in grid.legend.legendHandles:
    handle.set_alpha(0.8)
    handle.set_sizes([40])
    
for text in grid._legend.get_texts():
    text.set_color("white")
    
plt.show()
plt.savefig('Figure_export/xxx.png', dpi=600, bbox_inches='tight')