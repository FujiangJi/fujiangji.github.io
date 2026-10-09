import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
from scipy import stats
import cartopy.io.shapereader as shpreader
warnings.filterwarnings('ignore')

def log_log_regression_model(log_x):
    return intercept + slope * log_x

#*************************
file_name = "/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/Country_Forest_Area_Edge.csv"
df = pd.read_csv(file_name)
df.dropna(inplace = True)

# Calculating residuals for 2000
log_forest_area = np.log(df["Total Forest Area 2000 (KM2)"])
log_forest_edge = np.log(df["Total Forest Edge Length 2000 (KM)"])
slope, intercept, r_value, p_value, std_err = stats.linregress(log_forest_area, log_forest_edge)

log_estimated_forest_edge = log_log_regression_model(log_forest_area)
estimated_forest_edge = np.exp(log_estimated_forest_edge)
df['log_residuals2000'] = log_forest_edge - log_estimated_forest_edge

# Calculating residuals for 2020
log_forest_edge_2020 = np.log(df["Total Forest Edge Length 2020 (KM)"])
log_forest_area_2020 = np.log(df["Total Forest Area 2020 (KM2)"])
log_estimated_forest_edge_2020 = log_log_regression_model(log_forest_area_2020)
estimated_forest_edge_2020 = np.exp(log_estimated_forest_edge_2020)
df['log_residuals2020'] = log_forest_edge_2020 - log_estimated_forest_edge_2020

# Calculating delta residuals
df['delta_residuals'] = df['log_residuals2020'] - df['log_residuals2000']
# Output the results of the regression and the residuals
# slope, np.exp(intercept), r_value ** 2, p_value, df[['Country', 'log_residuals2000', 'log_residuals2020', 'delta_residuals']].head()

# Load the shapefile using Cartopy
shapefile = shpreader.natural_earth(resolution='110m', category='cultural', name='admin_0_countries')
reader = shpreader.Reader(shapefile)
# Create a dictionary mapping from country names to continents
country_to_continent = {country.attributes['NAME_LONG']: country.attributes['CONTINENT'] for country in reader.records()}
# Map each country in your dataframe to its continent
df['continent'] = df['Country'].map(country_to_continent)

# Define colors for each continent
colors = {
    'Asia': 'red',
    'Africa': 'green',
    'North America': 'blue',
    'South America': 'yellow',
    'Europe': 'purple',
    'Oceania': 'cyan',
    'Antarctica': 'white'
}
# Map continents to colors in the dataframe
df['color'] = df['continent'].map(colors)
df.dropna(inplace = True)

fig,ax = plt.subplots(figsize = (7,4.5))
config = {"font.family":'Helvetica'}
plt.subplots_adjust(hspace =0.2,wspace =0.2)
plt.rcParams.update(config)

for continent, group in df.groupby('continent'):
    ax.scatter(group['log_residuals2000'], group['delta_residuals'], color=group['color'], alpha=0.5, label=continent)

ax.axhline(0, color='red', linestyle='--', lw=3)
ax.axvline(0, color='red', linestyle='--', lw=3)
ax.set_xlabel('Edge Length Residuals at Log Scale in 2000 (log(km))' ,fontsize=10)
ax.set_ylabel('Δ Edge Length Residuals at Log Scale (log(km))',fontsize=10)

ax.tick_params(axis='both',which='major',labelsize=11,direction='out',length=3,width=0.5,pad=1.3,labelleft = True, labelbottom = True,
            bottom=True,left=True,top=False,right=False)

ax.legend(title="Continent" ,title_fontsize='large', scatterpoints=1, loc = 'upper right',fontsize=10)
plt.savefig('/scratch/fji7/Forest_edge_mapping_2024_11_14/2_exported_figures/Figure S6_unequal development of forest landscape patterns.png', dpi=1000, bbox_inches='tight')