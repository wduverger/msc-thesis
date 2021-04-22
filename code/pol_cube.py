# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


linewidth = (210-50)*.03937
figwidth = linewidth / 2
figheight = 4.8 / 6.4 * figwidth 
plt.rcParams['font.size'] = '6'

data = pd.read_csv(
    r'..\data\21-03-09 - pol cube on test bench.csv', sep=';', 
    header=1, decimal=',', skipfooter=4, engine='python'
)

fig, ax = plt.subplots(figsize=(figwidth, figheight))

ax.plot(data['pol angle'], data['pT/max'], '.-', label='Transmitted')
ax.plot(data['pol angle'], data['pR/max'], '.-', label='Reflected')
ax.set(
    xlabel='Incoming polarisation (deg)',
    xticks=np.arange(0,181, 30),
    ylabel='Power (normalised)',
)
ax.legend()

fig.savefig('../figures_generated/pol_cube.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/pol_cube.svg', bbox_inches='tight')
