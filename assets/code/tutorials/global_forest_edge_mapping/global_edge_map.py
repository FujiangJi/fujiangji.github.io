from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from scipy.ndimage import zoom
import matplotlib.ticker as mtick
import matplotlib as mpl
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.image as mpimg
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def read_data(image_data):
    dataset = gdal.Open(image_data)
    geotransform = dataset.GetGeoTransform()
    origin_x,origin_y = geotransform[0],geotransform[3]
    pixel_width, pixel_height = geotransform[1],geotransform[5]
    
    width, height = dataset.RasterXSize, dataset.RasterYSize
    lon = origin_x + pixel_width * np.arange(width)
    lat = origin_y + pixel_height * np.arange(height)
    
    data = dataset.GetRasterBand(1).ReadAsArray()
    if data.max()>10000:
        data = data/1000
    data[data < 0.01] = np.nan
    return data,lon,lat

def read_tif(tif_file):
    dataset = gdal.Open(tif_file)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    im_proj = (dataset.GetProjection())
    im_Geotrans = (dataset.GetGeoTransform())
    im_data = dataset.ReadAsArray(0, 0, cols, rows)
    if im_data.ndim == 3:
        im_data = np.moveaxis(dataset.ReadAsArray(0, 0, cols, rows), 0, -1)
    dataset = None
    return im_data, im_Geotrans, im_proj,rows, cols

def base_map(ax):
    states_provinces = cf.NaturalEarthFeature(category='cultural',name='admin_1_states_provinces_lines',
                                              scale='50m',facecolor='none')
    ax.add_feature(cf.LAND,alpha=0.2)
    ax.add_feature(cf.BORDERS, linestyle='--',lw=0.4, alpha=0.5)
    ax.add_feature(cf.LAKES, alpha=0.5)
    ax.add_feature(cf.COASTLINE,lw=0.5)
    ax.add_feature(cf.RIVERS,lw=0.2)
    ax.add_feature(states_provinces,lw=0.2,edgecolor='gray')
    return

def lon_lat_stats(im_data, lon, lat):
    lon_sum, lat_sum = np.nansum(im_data, axis = 0), np.nansum(im_data, axis = 1)
    lon_sum = np.split(lon_sum, len(lon_sum)/10)
    lon_sum = np.array([subarray.sum() for subarray in lon_sum])
    lat_sum = np.split(lat_sum, len(lat_sum)/10)
    lat_sum = np.array([subarray.sum() for subarray in lat_sum])
    lat_statistical,lon_statistical = zoom(lat,0.1),zoom(lon,0.1)
    return lat_statistical,lon_statistical, lat_sum, lon_sum

data1,lon,lat = read_data(f"/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/2000Edge.tif")
data2,lon,lat = read_data(f"/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/2020Edge.tif")
data = data2-data1

lat_statistical1,lon_statistical1, lat_sum1, lon_sum1 = lon_lat_stats(data1, lon, lat)
lat_statistical,lon_statistical, lat_sum, lon_sum = lon_lat_stats(data, lon, lat)

###
ex1,_,_,_,_ = read_tif(f"/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/Example_extent.tif")
ex2,_,_,_,_ = read_tif(f"/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/Example_edge.tif")
img = mpimg.imread('/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/conceptual_figure.png')

ex1 = ex1[50:200, 95:272]
ex2 = ex2[50:200, 95:272]

df = pd.read_csv("/scratch/fji7/Forest_edge_mapping_2024_11_14/1_data/Country_Forest_Area&Edge.csv")
years = [2000, 2005, 2010, 2015, 2020]
statis = df.sum(axis = 0)

areas = [statis[f"Total Forest Area {year} (KM2)"] for year in years]
edges = [statis[f"Total Forest Edge Length {year} (KM)"] for year in years]
years = [str(year) for year in years]

#************************************************************************************************************************************************************************************************
print("start plotting")
fig = plt.figure(figsize = (10,8))
config = {"font.family":'Helvetica'}
plt.subplots_adjust(hspace =0.3)
plt.rcParams.update(config)

# plot 2000 edge and 2020~2000 edge differences.
ax1 = fig.add_subplot(2,1,1,projection = ccrs.Robinson(central_longitude=0.0))
ax2 = fig.add_subplot(2,1,2,projection = ccrs.Robinson(central_longitude=0.0))

base_map(ax1)
base_map(ax2)

ax1.tick_params(axis='both',which='major',labelsize=8,direction='out',length=3,width=0.5,pad=1.3,labelleft = False, labelbottom = False,
                bottom=False,left=False,top=False,right=False)
ax2.tick_params(axis='both',which='major',labelsize=8,direction='out',length=3,width=0.5,pad=1.3,labelleft = False, labelbottom = False,
                bottom=False,left=False,top=False,right=False)

ax1.spines['geo'].set_linewidth(0)
ax2.spines['geo'].set_linewidth(0)
lons, lats = np.meshgrid(lon, lat)

### 2000 edges
cmap = 'YlGnBu'
max_value = 0
min_value = 15
lev = np.arange(0,15.1,5)
ax1.text(-0.05,1.05, f'B. Global Forest Edge in 2000', transform=ax1.transAxes, fontsize = 9,fontweight='bold')
ax1.set_extent([-179.99, 179.99, lat.min(), lat.max()])        
      
p = ax1.pcolormesh(lons,lats,data1,transform=ccrs.PlateCarree(),cmap=cmap,vmin = min_value, vmax = max_value)

cax, kw = mpl.colorbar.make_axes(ax1, location='bottom', pad=0.06, shrink=0.15,anchor = (0.98,0.65))
cbar = plt.colorbar(p, cax=cax, orientation='horizontal',ticks=lev)
cbar.ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
cbar.outline.set_visible(False)
cbar.ax.tick_params(labelsize=7,pad = 0.1,length=1)
cbar.set_label('Forest edge length (km)',fontsize = 8,labelpad=2)

### 2000~ 2020 edges differences
cmap = 'coolwarm'
max_value = 2
min_value = -2
lev = np.arange(-2,2.1,1)
ax2.text(-0.05,1.05, f'C. Global Forest Edge Difference: 2020 - 2000 ', transform=ax2.transAxes, fontsize = 9,fontweight='bold')
ax2.set_extent([-179.99, 179.99, lat.min(), lat.max()])        
        
p = ax2.pcolormesh(lons,lats,data,transform=ccrs.PlateCarree(),cmap=cmap,vmin = min_value, vmax = max_value)

cax, kw = mpl.colorbar.make_axes(ax2, location='bottom', pad=0.06, shrink=0.15,anchor = (0.95,0.65))
cbar = plt.colorbar(p, cax=cax, orientation='horizontal',ticks=lev)
cbar.ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
cbar.outline.set_visible(False)
cbar.ax.tick_params(labelsize=7,pad = 0.1,length=1)
cbar.set_label(r"$\Delta$ Forest edge length (km)",fontsize = 8,labelpad=2)

"""
***************************************************************************************************
"""
ax1_inset1 = inset_axes(ax1, width="100%", height="40%", loc='lower center', bbox_to_anchor=(0, -0.35, 1, 1),bbox_transform=ax1.transAxes)
ax1_inset2 = inset_axes(ax1, width="15%", height="100%", loc='center right', bbox_to_anchor=(0.2, 0, 1, 1),bbox_transform=ax1.transAxes)

###
ax1_inset1.plot(lon_statistical1, lon_sum1, c = 'dodgerblue', lw = 1.5)
ax1_inset1.set_xlim(lon.min(),lon.max())
ax1_inset1.xaxis.set_major_formatter(LongitudeFormatter())     
ax1_inset1.set_facecolor('none')
ax1_inset1.tick_params(axis='both',which='major',labelsize=7,direction='in',pad=1,bottom=True, left=True,top=False,right=False)
ax1_inset1.spines[['top', 'right']].set_visible(False)
ax1_inset1.set_xlabel('Longitude',fontsize = 8,labelpad = 5)
ax1_inset1.set_ylabel(r"Forest edge length (km) $\times 10^5$",fontsize = 8,labelpad = 5)
ax1_inset1.ticklabel_format(style='scientific', scilimits=(0, 0), axis='y')
ax1_inset1.yaxis.offsetText.set_visible(False)

###
ax1_inset2.plot(lat_sum1,lat_statistical1, c = 'dodgerblue', alpha=0.8,lw = 1.5)
ax1_inset2.set_facecolor('none')
ax1_inset2.spines[['bottom', 'right']].set_visible(False)
ax1_inset2.tick_params(axis='both',which='major',labelsize=7,direction='in',labeltop=True, 
                labelbottom=False,pad=1,bottom=False, left=True,top=True,right=False)
ax1_inset2.xaxis.set_label_position('top')
ax1_inset2.set_ylim(lat.min(),lat.max())
ax1_inset2.set_xlabel(r"Forest edge length (km) $\times 10^5$",fontsize = 8,labelpad = 5)
ax1_inset2.set_ylabel('Latitude',fontsize = 8,labelpad = 5)
ax1_inset2.set_yticklabels([x.get_text() for x in ax1_inset2.get_yticklabels()],rotation=90, va='center')
ax1_inset2.yaxis.set_major_formatter(LatitudeFormatter())
ax1_inset2.ticklabel_format(style='scientific', scilimits=(0, 0), axis='x')
ax1_inset2.xaxis.offsetText.set_visible(False)

"""
***************************************************************************************************
"""
ax2_inset1 = inset_axes(ax2, width="100%", height="40%", loc='lower center', bbox_to_anchor=(0, -0.35, 1, 1),bbox_transform=ax2.transAxes)
ax2_inset2 = inset_axes(ax2, width="15%", height="100%", loc='center right', bbox_to_anchor=(0.2, 0, 1, 1),bbox_transform=ax2.transAxes)

###
ax2_inset1.plot(lon_statistical, lon_sum, c = 'dodgerblue', lw = 1.5)
ax2_inset1.set_xlim(lon.min(),lon.max())
ax2_inset1.xaxis.set_major_formatter(LongitudeFormatter())     
ax2_inset1.set_facecolor('none')
ax2_inset1.tick_params(axis='both',which='major',labelsize=7,direction='in',pad=1,bottom=True, left=True,top=False,right=False)
ax2_inset1.spines[['top', 'right']].set_visible(False)
ax2_inset1.set_xlabel('Longitude',fontsize = 8,labelpad = 5)
ax2_inset1.set_ylabel(r"$\Delta$ Forest edge length (km) $\times 10^4$",fontsize = 8,labelpad = 5)
ax2_inset1.ticklabel_format(style='scientific', scilimits=(0, 0), axis='y')
ax2_inset1.yaxis.offsetText.set_visible(False)

###
ax2_inset2.plot(lat_sum,lat_statistical, c = 'dodgerblue', alpha=0.8,lw = 1.5)
ax2_inset2.set_facecolor('none')
ax2_inset2.spines[['bottom', 'right']].set_visible(False)
ax2_inset2.tick_params(axis='both',which='major',labelsize=7,direction='in',labeltop=True, 
                labelbottom=False,pad=1,bottom=False, left=True,top=True,right=False)
ax2_inset2.xaxis.set_label_position('top')
ax2_inset2.set_ylim(lat.min(),lat.max())
ax2_inset2.set_xlabel(r"$\Delta$ Forest edge length (km) $\times 10^5$",fontsize = 8,labelpad = 5)
ax2_inset2.set_ylabel('Latitude',fontsize = 8,labelpad = 5)
ax2_inset2.set_yticklabels([x.get_text() for x in ax2_inset2.get_yticklabels()],rotation=90, va='center')
ax2_inset2.yaxis.set_major_formatter(LatitudeFormatter())
ax2_inset2.ticklabel_format(style='scientific', scilimits=(0, 0), axis='x')
ax2_inset2.xaxis.offsetText.set_visible(False)

"""
***************************************************************************************************
"""

axx1 = inset_axes(ax1, width="60%", height="70%", loc='upper left', bbox_to_anchor=(-0.14, 0.9, 1, 1),bbox_transform=ax1.transAxes)
axx2 = inset_axes(ax1, width="60%", height="70%", loc='upper center', bbox_to_anchor=(0.11, 0.9, 1, 1),bbox_transform=ax1.transAxes)
axx3 = inset_axes(ax1, width="60%", height="70%", loc='upper right', bbox_to_anchor=(0.36, 0.9, 1, 1),bbox_transform=ax1.transAxes)

axx1.imshow(ex1, cmap = "Greens_r", alpha = 0.6)
axx2.imshow(ex2, cmap = "Reds", alpha = 0.8)
axx3.imshow(img)

axx1.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False) 
axx2.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False) 
axx3.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)

ax1.text(-0.05,2, f'A. Workfolows for Forest Edge Mapping', transform=ax1.transAxes, fontsize = 9,fontweight='bold')
axx1.text(0,1.05, f'(A.1) Forest extents', transform=axx1.transAxes, fontsize = 7)
axx2.text(0,1.05, f'(A.2) Forest edges', transform=axx2.transAxes, fontsize = 7)
axx3.text(-0.1,1.05, f'(A.3) Conceptual of forest edge dynamics', transform=axx3.transAxes, fontsize = 7)

"""
***************************************************************************************************
"""
###
ax2.text(-0.05,-0.55, f'D. Forest Areas and Length Variations Over Time', transform=ax2.transAxes, fontsize = 9,fontweight='bold')
axx4 = inset_axes(ax2, width="120%", height="50%", loc='lower left', bbox_to_anchor=(0, -1.17, 1, 1),bbox_transform=ax2.transAxes)
axx4.plot(years, areas, color = "royalblue", marker = 'o',markersize=8,linewidth=3, label= r'Forest areas ($km^2$)')
axx4.set_xlabel('Year',fontsize = 10,labelpad = 1)
axx4.set_ylabel(r'Forest areas ($km^2$)', color='royalblue', fontsize = 8)
axx4.tick_params(axis='y', labelsize=8, labelcolor='royalblue')
axx4.ticklabel_format(style='scientific', scilimits=(0, 0), axis='y')
axx4.yaxis.offsetText.set_visible(False)
axx4.text(-0.02,1.02, r"$\times 10^7$", transform=axx4.transAxes, fontsize = 7, color = "royalblue")
axx4.legend(loc = 'upper right',fontsize=8, facecolor= 'none',edgecolor = 'none',bbox_to_anchor=(0.945, 1.05))

###
axx5 = inset_axes(ax2, width="120%", height="50%", loc='lower left', bbox_to_anchor=(0, -1.17, 1, 1),bbox_transform=ax2.transAxes)
axx5.set_facecolor('none')
axx5.plot(years, edges, color = "orangered", marker = 's',markersize=5,linewidth=3,ls = "-.", label='Forest edge length (km)')
axx5.set_ylabel(r'Forest edge length ($km$)', color='orangered', fontsize = 8)
axx5.tick_params(axis='y', labelcolor='royalblue')

axx5.spines[['top', 'left']].set_visible(False)
axx5.yaxis.set_label_position('right')
axx5.tick_params(axis='both',which='major',labelsize=8,direction='out',labeltop=False,labelright=True,labelleft=False,
                  labelbottom=False,pad=1,bottom=False, left=False,top=False,right=True)
axx5.tick_params(axis='y', labelcolor='orangered')
axx5.ticklabel_format(style='scientific', scilimits=(0, 0), axis='y')
axx5.yaxis.offsetText.set_visible(False)
axx5.text(0.98,1.02, r"$\times 10^8$", transform=axx5.transAxes, fontsize = 7, color = "orangered")
axx5.legend(loc = 'upper right',fontsize=8, facecolor= 'none',edgecolor = 'none',bbox_to_anchor=(1, 0.8))

plt.savefig('/scratch/fji7/Forest_edge_mapping_2024_11_14/2_exported_figures/Figure 1_Forest edge.png', dpi=1000, bbox_inches='tight')