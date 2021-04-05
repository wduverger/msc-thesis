# %%
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

import utils

linewidth = (210-50)*.03937
figwidth = linewidth
figheight = 4.8 / 6.4 * linewidth/2
plt.rcParams['font.size'] = '6'

# %%
msr = utils.read_msr('./data/21-03-22 - 5c my calibration with pol cube.msr')

# %%
fig, ax = plt.subplots(1,2, figsize=(figwidth, figheight), sharey=True, sharex=True)
x_axis=np.arange(0,171,10)
for i in range(4):
    ax[0].plot(x_axis, msr[f'apd1 {{{i}}}'].sum(axis=(1,2)), '.-', color=f'C{i}')
    ax[1].plot(x_axis, msr[f'apd2 {{{i}}}'].sum(axis=(1,2)), '.-', color=f'C{i}', label=i*45)
    
ax[0].set(
    title='APD1',
    xticks=np.arange(0,181,45),
    xlabel='Rotation angle (deg)',
    ylabel='Intensity at APD (au)'
)    
ax[1].set(
    title='APD2',
    xlabel='Rotation angle (deg)',
)
ax[1].legend(title='P1 angle')

fig.savefig('./figures/pol cube effects.pdf', bbox_inches='tight')

# %%
utils.shutdown_jvm()