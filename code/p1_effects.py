# %%
import utils

import numpy as np
import matplotlib.pyplot as plt

linewidth = (210-50)*.03937
figwidth = linewidth
figheight = 4.8 / 6.4 * linewidth/2
plt.rcParams['font.size'] = '6'

# %%
msr = utils.read_msr('../data/21-04-08 - 2 detector waveplate calibration.msr')

# %%
fig, ax = plt.subplots(
    1, 4, 
    figsize=(figwidth, .6*figheight), sharey=True, 
    sharex=True, gridspec_kw=dict(wspace=0.2)
)

im = lambda p1, p2: msr[f'p1_{p1}_p2_{p2}'].sum(axis=(1,2))
x_axis=np.arange(0,161,20)

for p2 in [0,45,90,135]:
    ax[0].plot(x_axis, im(p1=0, p2=p2))
    ax[1].plot(x_axis, im(p1=45, p2=p2))
    ax[2].plot(x_axis, im(p1=90, p2=p2))
    ax[3].plot(x_axis, im(p1=135, p2=p2), label=p2)
    

ax[0].set(
    xticks=np.arange(0,181,45),
    xlabel='Control angle (deg)',
    ylabel='Intensity after P2 (au)'
)    
for i in range(4):
    ax[i].set(
        title=f'P1 = {i*45}',
        xlabel=ax[0].get_xlabel(), 
        xticks=ax[0].get_xticks())
ax[3].legend(title='P2 angle', loc='upper right')

fig.savefig('../figures_generated/p1_effects.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/p1_effects.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()
