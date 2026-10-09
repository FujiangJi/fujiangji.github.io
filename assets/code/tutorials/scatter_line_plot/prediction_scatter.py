import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

def d(x,y):
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    return z

# plot a 2*3 axes figure with 100 dpi.
fig = plt.figure(figsize=(10.5,6), dpi=100)
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.2)
plt.rcParams.update(config)

# basic information used in the figure, including the x/y lim, units, accuracy, text location, etc.
lims = {'Chla+b':90,'Ccar':22,'LMA':350}
units = {'Chla+b':'($\mu g/cm^2$)','Ccar':'($\mu g/cm^2$)','LMA':'($g/m^2$)'}
R2_mean = [0.75, 0.598, 0.735, 0.331, 0.285, 0.584]
R2_std = [0.01, 0.06, 0.08, 0.01, 0.04, 0.13]
RMSE_mean = [6.13, 1.33, 14.11, 8.04, 1.67, 17.53]
RMSE_std = [0.55, 0.14, 6.55, 1.19, 0.17, 7.87]
NRMSE_mean = [12.9, 14.58, 12.53, 24.45, 23.06, 18.8]
NRMSE_std = [0.14, 1.81,3.35, 0.71, 2.39, 6.67]
text_loc = [[0.02,0.02,0.02,0.83,0.75,0.67], [0.02,0.02,0.02,0.83,0.75,0.67],[0.02,0.02,0.02,0.83,0.75,0.67],
            [0.02,0.02,0.02,0.83,0.75,0.67], [0.02,0.02,0.02,0.83,0.75,0.67], [0.02,0.02,0.02,0.83,0.75,0.67]]
title1 = ['(a)','(b)', '(c)','(d)','(e)','(f)']
title2 = ['Random','Random','Random','Temporal','Temporal', 'Temporal']

# open the dataset.
df = pd.read_csv("data/trait_estimation.csv")

i = 0
for cv in df["CV_methods"].unique():
    for tr in df["tr_estimation"].unique():
        ax = fig.add_subplot(2,3,i+1)

        data = df[(df["CV_methods"]==cv)&(df["tr_estimation"]==tr)]

        dff = data[(df['final_model_result']>0)&(data[tr]>0)]
        x,y = dff['final_model_result'], dff[tr]

        # plot the error bars.
        iteration_df = dff.loc[:,'iteration_1':'iteration_100']
        mean_all,std_all = np.mean(iteration_df,1), np.std(iteration_df,1)
        lc_all,hc_all = mean_all-1.96*std_all,mean_all+1.96*std_all
        x_right, x_left = hc_all - x, x - lc_all

        scatter = ax.scatter(x, y,  c= d(x,y), s=4,cmap='rainbow',zorder = 2)
        ax.errorbar(x,y, xerr=(x_left, x_right),fmt='.',color = 'none',ecolor='k',elinewidth=0.4,zorder = 1)

        ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='k', lw = 1.5,label = '1:1 line')
        cbar = plt.colorbar(scatter, ax=ax,pad=0.01, shrink=0.9)
        ax.text(1.02,0.98,'High',transform=ax.transAxes,fontsize = 8)
        ax.text(1.02,-0.02,'Low',transform=ax.transAxes,fontsize = 8)
        cbar.set_ticks([])
        cbar.set_label('Density', fontsize=9,labelpad=0.1)

        ax.set_xlim(0,lims[tr])
        ax.set_ylim(0,lims[tr])
        ax.set_xlabel(f'Predicted {tr} {units[tr]}', fontsize=10, labelpad = 0.2)
        ax.set_ylabel(f'Observed {tr} {units[tr]}', fontsize=10, labelpad = 0.2)
        ax.tick_params(axis='both', direction='out', labelsize=10)

        R2_ = f'$R^2$ = {R2_mean[i]}\u00B1{R2_std[i]}'
        RMSE_ = f'$RMSE$ = {RMSE_mean[i]}\u00B1{RMSE_std[i]} {units[tr][2:-1]}'
        NRMSE_ = f'$NRMSE$ = {NRMSE_mean[i]}%\u00B1{NRMSE_std[i]}%'

        ax.text(text_loc[i][0],text_loc[i][3],R2_, fontsize=8,transform=ax.transAxes)
        ax.text(text_loc[i][1],text_loc[i][4],RMSE_, fontsize=8,transform=ax.transAxes)
        ax.text(text_loc[i][2],text_loc[i][5],NRMSE_, fontsize=8,transform=ax.transAxes)
        ax.text(0.02,0.93, f'{title1[i]} {tr}: {title2[i]} 5-fold CV', transform=ax.transAxes, fontsize = 8,fontweight='bold') 
        i = i+1
plt.savefig('Figure_export/xxx.png', dpi=600, bbox_inches='tight')