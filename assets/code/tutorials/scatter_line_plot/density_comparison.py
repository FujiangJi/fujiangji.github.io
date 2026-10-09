import scipy.io as scio
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

def d(x,y):
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    return z

def fit_line(x, y):
    line_fit = np.polyfit(x, y, 1)
    return line_fit[0],line_fit[1]

def sca_plot(ax,x1,x2,y1,y2,variable1,variable2,ylim):
    x1 = pd.DataFrame(x1.reshape(1,-1)[0],columns = [variable1])
    x2 = pd.DataFrame(x2.reshape(1,-1)[0],columns = [variable1])
    y1 = pd.DataFrame(y1.reshape(1,-1)[0],columns = [variable2])
    y2 = pd.DataFrame(y2.reshape(1,-1)[0],columns = [variable2])

    df1 = pd.concat([x1,y1],axis = 1)
    df2 = pd.concat([x2,y2],axis = 1)
    df1.dropna(axis=0,how='any',inplace = True)
    df2.dropna(axis=0,how='any',inplace = True)
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='k', lw = 1.5)
    ax.scatter(df1[variable1],df1[variable2],c= d(df1[variable1],df1[variable2]), s=3,cmap='autumn',alpha = 0.07)
    ax.scatter(df2[variable1],df2[variable2],c= d(df2[variable1],df2[variable2]), s=3,cmap='winter',alpha = 0.05)

    sns.regplot(variable1,variable2, data = df1, ax = ax,fit_reg=True, ci = 95,scatter=False,line_kws = {'color':'orangered','lw':1.5})
    sns.regplot(variable1,variable2, data = df2, ax = ax,fit_reg=True, ci = 95,scatter=False,line_kws = {'color':'blue','lw':1.5})
    ax.set_xlabel(variable1, fontsize=9, labelpad = 0.2)
    ax.set_ylabel(variable2, fontsize=9, labelpad = 0.2)
    ax.set_ylim(ylim[0],ylim[1])
    ax.tick_params(labelsize=8)

    a1,b1 = fit_line(df1[variable1],df1[variable2])
    a2,b2 = fit_line(df2[variable1],df2[variable2])
    
    if (variable1 =='FPAR')&(variable2 =='SIF/PAR'):
        if b1>0:
            ax.text(0.02,0.9, f'$y$ = {str(round(a1,3))}$x$ + {str(round(b1,3))}', transform=ax.transAxes, fontsize = 8,c = 'orangered')
        else:
            ax.text(0.02,0.9, f'$y$ = {str(round(a1,3))}$x$ {str(round(b1,3))}', transform=ax.transAxes, fontsize = 8,c = 'orangered')

        if b2>0:
            ax.text(0.02,0.8, f'$y$ = {str(round(a2,3))}$x$ + {str(round(b2,3))}', transform=ax.transAxes, fontsize = 8,c = 'blue')
        else:
            ax.text(0.02,0.8, f'$y$ = {str(round(a2,3))}$x$ {str(round(b2,3))}', transform=ax.transAxes, fontsize = 8,c = 'blue')
    else:
        if b1>0:
            ax.text(0.4,0.12, f'$y$ = {str(round(a1,3))}$x$ + {str(round(b1,3))}', transform=ax.transAxes, fontsize = 8,c = 'orangered')
        else:
            ax.text(0.4,0.12, f'$y$ = {str(round(a1,3))}$x$ {str(round(b1,3))}', transform=ax.transAxes, fontsize = 8,c = 'orangered')

        if b2>0:
            ax.text(0.4,0.02, f'$y$ = {str(round(a2,3))}$x$ + {str(round(b2,3))}', transform=ax.transAxes, fontsize = 8,c = 'blue')
        else:
            ax.text(0.4,0.02, f'$y$ = {str(round(a2,3))}$x$ {str(round(b2,3))}', transform=ax.transAxes, fontsize = 8,c = 'blue')
    return

data = scio.loadmat('data/Figure_1_S2_S3_S4_S7_data.mat')
x_axis = [['LAI_cb','LAI_an'],['FPAR_cb','FPAR_an']]
y_axis = [['EVI_cb','EVI_an'],['NIRv_cb','NIRv_an'],['SIF_PAR_cb','SIF_PAR_an'],['NDVI_cb','NDVI_an']]

v1 = ['LAI','FPAR']
v2 = ['EVI','NIRv','SIF/PAR','NDVI']
#*************************************************************************
fig,ax = plt.subplots(2,4,figsize = (12,5))
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.3,hspace =0.22)
plt.rcParams.update(config)
y_lim = [[0.2,0.8],[0,0.5],[0,0.03],[0.4,1]]

for i in range(2):
    for j in range(4):
        x1,x2,y1,y2 = data[x_axis[i][0]],data[x_axis[i][1]],data[y_axis[j][0]],data[y_axis[j][1]]
        variable1,variable2 = v1[i],v2[j]
        print(i,j,x_axis[i][0],x_axis[i][1],y_axis[j][0],y_axis[j][1])
        print(variable1,variable2)
        print('--------------------')
        sca_plot(ax[i][j],x1,x2,y1,y2,variable1,variable2,y_lim[j])
ax[0][0].text(-0.25,0.9, 'a', transform=ax[0][0].transAxes, fontsize = 10,fontweight = 'bold')
plt.savefig('Figure_export/Extended Data Figure 3(a).png', dpi=600, bbox_inches='tight')