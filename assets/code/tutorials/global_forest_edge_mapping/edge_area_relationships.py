import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from scipy import stats
warnings.filterwarnings('ignore')

def rsquared(x, y): 
    """Return the metriscs coefficient of determination (R2)
    Parameters:
    -----------
    x (numpy array or list): Predicted variables
    y (numpy array or list): Observed variables
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y) 
    a = r_value**2
    return a

#*************************
file_name = "/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/Country_Forest_Area_Edge.csv"
df = pd.read_csv(file_name)
df.dropna(inplace = True)

x1, x2, x3, x4, x5 = df["Total Forest Edge Length 2000 (KM)"],df["Total Forest Edge Length 2005 (KM)"],df["Total Forest Edge Length 2010 (KM)"],df["Total Forest Edge Length 2015 (KM)"],df["Total Forest Edge Length 2020 (KM)"]
y1, y2, y3, y4, y5 = df["Total Forest Area 2000 (KM2)"],df["Total Forest Area 2005 (KM2)"],df["Total Forest Area 2010 (KM2)"],df["Total Forest Area 2015 (KM2)"],df["Total Forest Area 2020 (KM2)"]

fig,ax = plt.subplots(figsize = (5,4))
config = {"font.family":'Helvetica'}
plt.subplots_adjust(hspace =0.2,wspace =0.2)
plt.rcParams.update(config)

x = [x1, x2, x3, x4, x5]
y = [y1, y2, y3, y4, y5]
colors = ["orangered", "#35a153","#303cf9", "#979797", "dodgerblue"]
markers = ["P", "X", "^", "v", "o"]
years = ["2000", "2005", "2010", "2015", "2020"]

a_total = []
b_total = []
for idx in range(5):
    a,b = x[idx], y[idx]
    a_total.extend(a)
    b_total.extend(b)
    ax.scatter(a,b,color=colors[idx], label=years[idx], alpha=0.7, edgecolors='w', linewidth=0.5, marker = markers[idx],s = 50)
    
final = pd.DataFrame([a_total,b_total]).T
final.columns = ["edge","area"]
final = final[(final['edge'] > 0) & (final['area'] > 0)]
              
coeffs = np.polyfit(np.log(final['edge']), np.log(final['area']), 1)
ax.plot(final['edge'], np.exp(coeffs[1]) * final['edge'] ** coeffs[0], color='k', linestyle='-', linewidth=2)

R2 = rsquared(final['edge'], final['area'])
_, p_value = stats.ttest_ind(final['edge'], final['area'])

ax.text(0.02, 0.93, f"$R^2$ = {round(R2,3)}", transform=ax.transAxes, color='k', fontsize=12)
ax.text(0.02, 0.86, f"$p$ = {round(p_value,5)}", transform=ax.transAxes, color='k', fontsize=12)

ax.set_xlabel('Edge ($km$)',fontsize=12,labelpad = 1)
ax.set_ylabel('Area ($km^2$)',fontsize=12,labelpad = 1)
ax.legend(title='Year',title_fontsize='large', scatterpoints=1, loc = 'lower right',fontsize=12,facecolor= 'none',edgecolor = 'none')
ax.tick_params(axis='both',which='major',labelsize=12,direction='out',length=3,width=0.5,pad=1.3,labelleft = True, labelbottom = True,
            bottom=True,left=True,top=False,right=False)
ax.set_xscale('log')
ax.set_yscale('log')
              
plt.savefig('/scratch/fji7/Forest_edge_mapping_2024_11_14/2_exported_figures/Figure S5_forest edge_area relationships.png', dpi=1000, bbox_inches='tight')