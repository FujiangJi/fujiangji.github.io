import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

def PFT_extrapolation(ax1,ax2,df1,df2,color,tr):
    ax1.set_facecolor((0,0,0,0.0))
    ax2.set_facecolor((0,0,0,0.0))
    col1 = [col for col in df2.columns if any(df2[col] > 2)]
    df1.drop(columns=col1,inplace = True), df2.drop(columns=col1,inplace = True)
    df2 = df2*100
    
    d1,d2,dp1,dp2 = df1.values.T,df2.values.T,len(df1),len(df2)
    m1,m2 = np.mean(d1, 0),np.mean(d2, 0)
    
    lc1,hc1 = st.t.interval(0.95, dp1-1,loc=np.mean(d1, 0),scale=st.sem(d1))
    lc2,hc2 = st.t.interval(0.95, dp2-1,loc=np.mean(d2, 0),scale=st.sem(d2))
    
    x1 = np.linspace(1, dp1, num=dp1)
    x2 = np.linspace(1, dp2, num=dp2)
    
    ax1.plot(x1,m1,marker = 'o',markersize=4,linewidth=2,c = color,label = tr)
    ax2.plot(x2,m2,marker = 'o',markersize=4,linewidth=2,c = color,label = tr)
    
    ax1.fill_between(x1, lc1,hc1, alpha=0.1,color = color)
    ax2.fill_between(x2, lc2,hc2, alpha=0.1,color = color)
    
    ax1.set_xlabel('Number of PFTs trained',fontsize = 10, color = "white")
    ax2.set_xlabel('Number of PFTs trained',fontsize = 10, color = "white")
    ax1.set_ylabel('$R^2$',fontsize = 11, color = "white")
    ax2.set_ylabel('$NRMSE$(%)',fontsize = 11, color = "white")
    
    legend = ax1.legend(loc = 'lower right',facecolor= 'none',edgecolor = 'none',fontsize = 9)
    for text in legend.get_texts():
        text.set_color("white")
    legend = ax2.legend(loc = 'upper right',facecolor= 'none',edgecolor = 'none',fontsize = 9,bbox_to_anchor=(1, 0.95))
    for text in legend.get_texts():
        text.set_color("white")
    ax1.tick_params(labelsize=9, colors = "white")
    ax2.tick_params(labelsize=9, colors = "white")
    ax1.spines[['top', 'right', 'bottom','left']].set_color("white")
    ax2.spines[['top', 'right', 'bottom','left']].set_color("white")
    return

df = pd.read_csv("data/PFT_extrapolation.csv")

fig,(ax1,ax2) = plt.subplots(1,2,figsize = (10,3))
fig.set_facecolor('none')
fig.set_alpha(0)

plt.subplots_adjust(wspace =0.18)
config = {"font.family":'Calibri'}
plt.rcParams.update(config)

colors = {'Chla+b':'r','Ccar':'g','EWT':'b','LMA':'orange'}
trait_name = ['Chla+b','Ccar','EWT','LMA']

for tr in trait_name:
    data = df[df["tr"]==tr]
    df1 = data[data["metric"]=="R2"].iloc[:,:-2]
    df2 = data[data["metric"]=="NRMSE"].iloc[:,:-2]
    PFT_extrapolation(ax1,ax2,df1,df2,colors[tr],tr) 
ax1.text(0.02,0.93, '(a) $R^2$ for PFTs extrapolation', transform=ax1.transAxes, fontsize = 10, color = "white")
ax2.text(0.02,0.93, '(b) $NRMSE$ for PFTs extrapolation', transform=ax2.transAxes, fontsize = 10, color = "white") 