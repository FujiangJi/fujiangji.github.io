import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D
from sklearn.metrics import mean_squared_error

def rsquared(x, y): 
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y) 
    a = r_value**2
    return a

def d(x,y):
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    return z
  
refl_pro = pd.read_csv("data/2_PROSPECT_reflectance_LUT.csv")
refl_sip = pd.read_csv("data/1_SIP_reflectance_LUT.csv")

#***********************************************************************8
fig = plt.figure(figsize = (12,8))
gs = gridspec.GridSpec(19,8)
config = {"font.family":'Calibri'}
plt.subplots_adjust(wspace =0.7,hspace =2)
plt.rcParams.update(config)

### PROSPECT synthetic reflectance [0-7, 8-13, 14-19]
ax = plt.subplot(gs[0:7, 0:4])
wl = np.arange(450,2401)
for i in range(len(refl_pro)):
    temp = refl_pro.iloc[i]
    ax.plot(wl,temp,linewidth=0.05,c = 'gray', alpha = 0.05,zorder = 1)

m_all = np.mean(refl_pro,0)
std_all = np.std(refl_pro,0)
lc_all = np.percentile(refl_pro, 2.5, axis=0)
hc_all = np.percentile(refl_pro, 97.5, axis=0)
ax.fill_between(wl, lc_all,hc_all, alpha=0.1,color = 'orangered',label = '95% CI of mean reflectance',zorder = 2)
ax.plot(wl,m_all,linewidth=2,c = 'orangered',label = 'Mean reflectance',zorder = 3)

ax.set_xlabel('Wavelength (nm)', fontsize=9, labelpad = 0.2)
ax.set_ylabel('Reflectacne', fontsize=9, labelpad = 0.2)
ax.tick_params(labelsize=8)
legend_elements = [Line2D([0], [0], color='gray', lw=1.5, alpha=1, label='Simulated reflectance')]
handles, labels = ax.get_legend_handles_labels()
handles.extend(legend_elements)
labels.extend(['Simulated reflectance'])
ax.legend(handles=handles, labels=labels, loc = 'upper right',facecolor= 'none',edgecolor = 'none',fontsize=9)
ax.text(-0.07,1.03, 'A. RTMs synthetic reflectance', transform=ax.transAxes, fontsize = 9,fontweight='bold')
ax.text(0.01,0.94, '(A.1) PROSPECT synthetic reflectance', transform=ax.transAxes, fontsize = 8)

### Leaf-SIP synthetic reflectance
ax = plt.subplot(gs[0:7, 4:8])
wl = np.arange(450,2401)
for i in range(len(refl_sip)):
    temp = refl_sip.iloc[i]
    ax.plot(wl,temp,linewidth=0.05,c = 'gray', alpha = 0.05,zorder = 1)

m_all = np.mean(refl_sip,0)
std_all = np.std(refl_sip,0)
lc_all = np.percentile(refl_sip, 2.5, axis=0)
hc_all = np.percentile(refl_sip, 97.5, axis=0)
ax.fill_between(wl, lc_all,hc_all, alpha=0.1,color = 'b',label = '95% CI of mean reflectance',zorder = 2)
ax.plot(wl,m_all,linewidth=2,c = 'b',label = 'Mean reflectance',zorder = 3)
ax.set_xlabel('Wavelength (nm)', fontsize=9, labelpad = 0.2)
ax.set_ylabel('Reflectacne', fontsize=9, labelpad = 0.2)
ax.tick_params(labelsize=8)

legend_elements = [Line2D([0], [0], color='gray', lw=1.5, alpha=1, label='Simulated reflectance')]
handles, labels = ax.get_legend_handles_labels()
handles.extend(legend_elements)
labels.extend(['Simulated reflectance'])
ax.legend(handles=handles, labels=labels, loc = 'upper right',facecolor= 'none',edgecolor = 'none',fontsize=9)
ax.text(0.01,0.94, '(A.2) Leaf-SIP synthetic reflectance', transform=ax.transAxes, fontsize = 8)

####
models = ['PROSPECT','Leaf-SIP']
tr_name = ['Chla+b','Ccar','EWT','LMA']
cmaps = {'PROSPECT':'autumn','Leaf-SIP':'winter'}
colors = {'PROSPECT':'orangered','Leaf-SIP':'blue'}
units = {'Chla+b':' ($\mu g/cm^2$)','Ccar':' ($\mu g/cm^2$)','EWT':' ($g/m^2$)','LMA':' ($g/m^2$)'}
title1 =['(C.1)','(C.2)','(C.3)','(C.4)']
title2 =['(D.1)','(D.2)','(D.3)','(D.4)']

j = 0
for kk, tr in enumerate(tr_name):
    file_name = f'{tr}/1_PROSPECT_{tr}_ANN_LUT_pred.csv'
    df = pd.read_csv(file_name)
    x,y = df['ANN_pred'],df['LUT_obs']
    if (tr =='EWT')|(tr =='LMA'):
        x,y = df['ANN_pred']*10000,df['LUT_obs']*10000

    R2 = f'$R^2$ = {str(round(rsquared(x, y),2))}'
    rmse = f'$RMSE$ = {str(round(np.sqrt(mean_squared_error(x,y)),1))} {units[tr][2:-1]}'
    nrmse = '$NRMSE$ = '+'{:.1%}'.format(np.sqrt(mean_squared_error(x,y))/(y.max()-y.min()))

    ax = plt.subplot(gs[8:13, j:j+2])
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='k', lw = 1.5)
    scatter = ax.scatter(x,y,c= d(x,y), s=20,cmap='autumn',alpha = 0.3)
    sns.regplot('ANN_pred','LUT_obs', data = df, ax = ax,fit_reg=True, ci = 95,scatter=False,line_kws = {'color':'orangered','lw':1.5})

    ax.set_xlabel(f'Predicted {tr} {units[tr]}', fontsize=8, labelpad = 0.05)
    ax.set_ylabel(f'LUT {tr} {units[tr]}', fontsize=8, labelpad = 0.05)
    ax.text(-0.15,1.08, 'B. Leaf trait prediction using PROSPECT synthetic data', transform=ax.transAxes, fontsize = 9,fontweight='bold') if j==0 else None

    cbar = plt.colorbar(scatter, ax=ax,pad=0.02, shrink=0.9)
    ax.text(1.02,0.98,'High',transform=ax.transAxes,fontsize = 7)
    ax.text(1.02,-0.02,'Low',transform=ax.transAxes,fontsize = 7)
    cbar.set_ticks([])
    cbar.set_label('Density', fontsize=9,labelpad=0.1)

    ax.text(0.03,0.92,f'{title1[kk]} PROSPECT - {tr}', fontsize=8,transform=ax.transAxes)
    ax.text(0.365,0.22,R2, fontsize=7,transform=ax.transAxes)
    ax.text(0.365,0.14,rmse, fontsize=7,transform=ax.transAxes)
    ax.text(0.365,0.05,nrmse, fontsize=7,transform=ax.transAxes)
    ax.tick_params(labelsize=8,direction='in')
    j = j+2

j = 0
for kk, tr in enumerate(tr_name):
    file_name = f'{tr}/1_Leaf-SIP_{tr}_ANN_LUT_pred.csv'
    df = pd.read_csv(file_name)
    x,y = df['ANN_pred'],df['LUT_obs']
    if (tr =='EWT')|(tr =='LMA'):
        x,y = df['ANN_pred']*10000,df['LUT_obs']*10000

    R2 = f'$R^2$ = {str(round(rsquared(x, y),2))}'
    rmse = f'$RMSE$ = {str(round(np.sqrt(mean_squared_error(x,y)),1))} {units[tr][2:-1]}'
    nrmse = '$NRMSE$ = '+'{:.1%}'.format(np.sqrt(mean_squared_error(x,y))/(y.max()-y.min()))

    ax = plt.subplot(gs[14:19, j:j+2])
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='k', lw = 1.5)
    scatter = ax.scatter(x,y,c= d(x,y), s=20,cmap='winter',alpha = 0.3)
    sns.regplot('ANN_pred','LUT_obs', data = df, ax = ax,fit_reg=True, ci = 95,scatter=False,line_kws = {'color':'blue','lw':1.5})

    ax.set_xlabel(f'Predicted {tr} {units[tr]}', fontsize=8, labelpad = 0.05)
    ax.set_ylabel(f'LUT {tr} {units[tr]}', fontsize=8, labelpad = 0.05)
    ax.text(-0.15,1.08, 'C. Leaf trait prediction using Leaf-SIP synthetic data', transform=ax.transAxes, fontsize = 9,fontweight='bold') if j==0 else None

    cbar = plt.colorbar(scatter, ax=ax,pad=0.02, shrink=0.9)
    ax.text(1.02,0.98,'High',transform=ax.transAxes,fontsize = 7)
    ax.text(1.02,-0.02,'Low',transform=ax.transAxes,fontsize = 7)
    cbar.set_ticks([])
    cbar.set_label('Density', fontsize=9,labelpad=0.1)

    ax.text(0.03,0.92,f'{title2[kk]} Leaf-SIP - {tr}', fontsize=8,transform=ax.transAxes)
    ax.text(0.365,0.22,R2, fontsize=7,transform=ax.transAxes)
    ax.text(0.365,0.14,rmse, fontsize=7,transform=ax.transAxes)
    ax.text(0.365,0.05,nrmse, fontsize=7,transform=ax.transAxes)
    ax.tick_params(labelsize=8,direction='in')
    j = j+2

plt.savefig('1_Figures/2_pretrained_DNN.png', dpi=500, bbox_inches='tight')