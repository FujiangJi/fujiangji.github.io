import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import FormatStrFormatter

colors = {'Chla+b':'orangered','Ccar':'dodgerblue','EWT':"pink",'LMA':'limegreen'}
colors2 = {'Chla+b':'blue','Ccar':'red','EWT':"green",'LMA':'orange'}
units = {'Chla+b':' ($\mu g/cm^2$)','Ccar':' ($\mu g/cm^2$)','EWT':' ($g/m^2$)','LMA':' ($g/m^2$)'}
site_label = {'Chla+b':[r"$S_{chl1}$",r"$S_{chl2}$",r"$S_{chl3}$",r"$S_{chl4}$",r"$S_{chl5}$",r"$S_{chl6}$",r"$S_{chl7}$",r"$S_{chl8}$"],
              'Ccar':[r"$S_{car1}$",r"$S_{car2}$",r"$S_{car3}$",r"$S_{car4}$",r"$S_{car5}$"],
              'EWT':[r"$S_{ewt1}$",r"$S_{ewt2}$",r"$S_{ewt3}$",r"$S_{ewt4}$"],
              'LMA':[r"$S_{lma1}$",r"$S_{lma2}$",r"$S_{lma3}$",r"$S_{lma4}$",r"$S_{lma5}$",r"$S_{lma6}$",
                     r"$S_{lma7}$",r"$S_{lma8}$",r"$S_{lma9}$",r"$S_{lma10}$",r"$S_{lma11}$",r"$S_{lma12}$"]}
pft_label = {'Chla+b':['DBF',"CRP","GRA"],'Ccar':['DBF',"CRP","GRA"],
              'EWT':['DBF',"CRP","GRA"],'LMA':['DBF',"CRP","GRA","SHR","vine","EBF","ENF"]}
temp_label = {'Chla+b':['EGS','PGS','PPS'],'Ccar':['EGS','PGS','PPS'],'LMA':['EGS','PGS','PPS']}

data_type = ["sites","PFT","temporal"]

fig = plt.figure(figsize = (14,15))
gs = gridspec.GridSpec(124, 80)

config = {"font.family":'Calibri'}
plt.subplots_adjust(wspace =0,hspace = 0)
plt.rcParams.update(config)

j = 0
for ds in data_type:
    tr_name = ["Chla+b","Ccar","LMA","EWT"] if ds !="temporal" else ["Chla+b","Ccar","LMA"]
    m = 0
    for tr in tr_name:
        data = pd.read_csv(f"../0_datasets/{tr}_dataset_{ds}.csv")
        df, refl = data.loc[:,"Dataset ID":], data.loc[:,"450":"2400"]
        
        ax = plt.subplot(gs[j:j+16, m:m+16])
        axes = plt.subplot(gs[j+20:j+36, m:m+14])
        axes1 = axes.twinx()
        
        wl_min = '450'
        wl_max = '2400'
        d_all = refl.loc[:,wl_min:wl_max].values
        m_all = np.mean(d_all,0)
        std_all = np.std(d_all,0)
        lc_all,hc_all = m_all-1.96*std_all,m_all+1.96*std_all
        CV = refl.loc[:,wl_min:wl_max].std()/refl.loc[:,wl_min:wl_max].mean()
        wl = np.arange(int(wl_min),int(wl_max)+1,10)
        
        axes.plot(wl,m_all,linewidth=2,color = colors[tr], label = "mean reflectance")
        axes.fill_between(wl, lc_all,hc_all, alpha=0.2,color = colors[tr])
        axes1.plot(wl,savgol_filter(CV,25,3),linewidth=2,ls = '--',color = colors2[tr],label = "mean CV")

        lines, labels = axes.get_legend_handles_labels()
        lines2, labels2 = axes1.get_legend_handles_labels()
        axes.legend(lines + lines2, labels + labels2, loc = 'upper right',facecolor= 'none',
                    edgecolor = 'none',fontsize=8,bbox_to_anchor=(0.98, 1.03))
    
        axes.set_xlabel('Wavelength (nm)',fontsize = 9,labelpad = 3)
        axes.set_ylabel(f"{tr} Reflectance", fontsize=9, labelpad = 0.2)
        axes1.set_ylabel("Coefficient of variation", fontsize=9, labelpad =0.2)

        axes.tick_params(labelsize=9, direction = 'in')
        axes1.tick_params(labelsize=9, direction = 'in')
        
        axes.yaxis.set_major_formatter(FuncFormatter(no_negative))
        axes1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
           
        if ds == "sites":
            site_info = df.groupby("Site ID")["Latitude","Longitude"].mean().sort_values(by='Latitude')
            site_info['Latitude'] = site_info['Latitude'].round(2)
            site_info['Longitude'] = site_info['Longitude'].round(2)
            site_info['coordinate'] = site_info.apply(lambda row: (row['Latitude'], row['Longitude']), axis=1)
            
            df_map = pd.DataFrame({'Site ID':site_info.index.tolist()})
            sort_map = df_map.reset_index().set_index('Site ID')
            df['Site_idx'] = df['Site ID'].map(sort_map['index'])
            df.sort_values(by = ['Site_idx'],inplace = True)
            df.reset_index(drop = True, inplace = True) 
            
            width = {'Chla+b':0.7,'Ccar':0.6,'EWT':0.6,'LMA':0.7}
            sns.boxplot(x= 'Site ID', y= tr,data=df, color=colors[tr],ax = ax, fliersize=0.5,saturation = 0.8,linewidth = 0.5, whis =2,width = width[tr])
            
            ax.set_xlabel(f'Site number of {tr} samples',fontsize = 9,labelpad = 3)
            ax.set_ylabel(tr+ units[tr], fontsize=9, labelpad = 0.2)
            ax.tick_params(labelsize=9, direction = 'in')
            ax.set_xticklabels(site_label[tr])
            if tr == "LMA":
                ax.tick_params(axis = "x", labelsize=7, direction = 'in',pad = -0.5, rotation=35)
                ax.set_xlabel(f'Site number of {tr} samples',fontsize = 9,labelpad = -3)

            ax.text(-0.13,1.05, 'A. Spatial dataset', fontsize=10,transform=ax.transAxes,weight='bold') if tr == "Chla+b" else None
            
        elif ds == "PFT":
            df_map = pd.DataFrame({'PFT':['Deciduous broadleaf forests', 'Croplands', 'Grasslands',
                                          'Shrublands','Vine','Evergreen broadleaf forests',
                                          'Evergreen needleleaf forests']}) if tr == "LMA" else pd.DataFrame({'PFT':['Deciduous broadleaf forests', 'Croplands', 'Grasslands']})
            
            sort_map = df_map.reset_index().set_index('PFT')
            df['PFT_idx'] = df['PFT'].map(sort_map['index'])
            df.sort_values(by = ['PFT_idx'],inplace = True)
            df.reset_index(drop = True, inplace = True) 
            
            width = {'Chla+b':0.45,'Ccar':0.45,'EWT':0.45,'LMA':0.7}
            sns.boxplot(x= 'PFT', y= tr,data=df, color=colors[tr],ax = ax, fliersize=0.5,saturation = 0.8,linewidth = 0.5, whis =2,width = width[tr])
            ax.set_xlabel(f'PFT',fontsize = 9,labelpad = 3)
            ax.set_ylabel(tr+ units[tr], fontsize=9, labelpad = 0.2)
            ax.tick_params(labelsize=9, direction = 'in')
            ax.set_xticklabels(pft_label[tr])
            ax.text(-0.13,1.05, 'B. PFT dataset', fontsize=10,transform=ax.transAxes,weight='bold') if tr == "Chla+b" else None
            
        else:
            df_map = pd.DataFrame({'season':['early growing season','peak growing season','post-peak season']})
            sort_map = df_map.reset_index().set_index('season')
            df['season_idx'] = df['season'].map(sort_map['index'])
            df.sort_values(by = ['season_idx'],inplace = True)
            df.reset_index(drop = True, inplace = True) 
            
            sns.boxplot(x= 'season', y= tr,data=df, color=colors[tr],ax = ax, fliersize=0.5,saturation = 0.8,linewidth = 0.5, whis =2,width = 0.5)
            ax.set_xlabel(f'Seasons',fontsize = 9,labelpad = 3)
            ax.set_ylabel(tr+ units[tr], fontsize=9, labelpad = 0.2)
            ax.tick_params(labelsize=9, direction = 'in')
            ax.set_xticklabels(temp_label[tr])
            ax.text(-0.13,1.05, 'C. Temporal dataset', fontsize=10,transform=ax.transAxes,weight='bold') if tr == "Chla+b" else None
            text = ('• DBF: Deciduous broadleaf forests\n'
                    '• CRP: Croplands\n'
                    '• GRA: Grasslands\n'
                    '• SHR: Shrublands\n'
                    '• EBF: Evergreen broadleaf forests\n'
                    '• ENF: Evergreen needleleaf forests\n'
                    '• EGS: Early growing season\n'
                    '• PGS: Peak growing season\n'
                    '• PPS: Post-peak season\n')
            ax.text(1.1,-0.5, text,fontsize=10,transform=ax.transAxes,linespacing=1.5) if tr == "LMA" else None       
        m = m+20
    j = j+42   
plt.savefig(f'1_Figures/1_leaf traits variations.png', dpi=500, bbox_inches='tight')