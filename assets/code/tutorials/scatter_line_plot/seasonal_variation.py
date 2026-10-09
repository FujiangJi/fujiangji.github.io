import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

# open the data.
df = pd.read_csv("data/seasonal_traits.csv")

# basic information used in the figure
tr_name = ["Chla+b", "Ccar","EWT", "Nitrogen"]
units = {'Chla+b':' ($\mu g/cm^2$)','Ccar':' ($\mu g/cm^2$)','EWT':' ($g/m^2$)', "Nitrogen":" ($\mu g/cm^2$)"}
title = ["(a)","(b)","(c)","(d)"]
styles = {"BART":{'linestyle': (0, (3, 1, 1, 1, 1, 1)), 'marker': 'o', "color":'#FF0000'},
          "HARV":{'linestyle': (0, (5, 1)), 'marker': 's', "color":'#FFA500'},
          "SCBI":{'linestyle': ":", 'marker': '^', "color":'#CCCC00'},
          "MLBS":{'linestyle': "-.", 'marker': '*', "color":'#0000FF'},
          "ORNL":{'linestyle': '-', 'marker': 'X', "color":'#4B0082'},
          "TALL":{'linestyle': (0, (3, 1, 1, 1)), 'marker': 'p', "color":'#EE82EE'}}

#******************************************************************************
fig = plt.figure(figsize = (12,6))
fig.set_facecolor('none')  # Make figure background transparent
fig.set_alpha(0)      
config = {"font.family":'Helvetica'}
plt.subplots_adjust(wspace =0.18, hspace =0.05)
plt.rcParams.update(config)

s = df["site"].unique()
style = {key: styles[key] for key in s}

# loop the traits for plotting
for i, tr in enumerate(tr_name):
    ax = fig.add_subplot(2,2,i+1)
    ax.set_facecolor((0,0,0,0.0))
    ax.grid(color='gray', linestyle=':', linewidth=0.3)

    kk = 0
    for site in s:
        df_temp = df[df["site"]==site]

        df_temp["month"] = df_temp["month"].astype(int)
        df_temp = df_temp.sort_values(by='month')

        x1,y1 = df_temp["month"],df_temp[f"{tr}_mean"]
        lc1,hc1 = df_temp[f"{tr}_mean"]-df_temp[f"{tr}_std"], df_temp[f"{tr}_mean"]+df_temp[f"{tr}_std"]
        ax.plot(x1,y1,label = site, markersize = 6,linewidth=2, **style[site])
        ax.fill_between(x1, lc1,hc1, alpha=0.1,color = style[site]["color"])
        kk = kk+1

    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_xlabel(f'Months', fontsize=11, labelpad = 6, color = "white")     
    ax.set_ylabel(f'PRISMA derived \n{tr} {units[tr]}', fontsize=11, color = "white")     
    ax.tick_params(labelsize=11,direction='in', colors = "white")
    ax.spines[['top', 'right', 'bottom','left']].set_color("white")
    ax.text(0.01,0.92,f"{title[i]} monthly -- {tr} -- DBF", fontsize=11,transform=ax.transAxes, color = "white")
    legend = ax.legend(loc='lower right',fontsize=10, facecolor= 'none',edgecolor = 'none',bbox_to_anchor=(1, -0.01),ncol= 2)
    for text in legend.get_texts():
        text.set_color("white")
    
    if (i != 2)&(i != 3):
        ax.set_xticklabels([])
        ax.set_xlabel('')
    if i !=0:
        ax.get_legend().remove()
plt.savefig('Figure_export/xxx.png', dpi=600, bbox_inches='tight')