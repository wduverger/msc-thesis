# %%

import matplotlib.pyplot as plt
import numpy as np

import utils

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

folder = r'G:\New_OutLab\JonasSted\D-disken\User data\Wouter\2021-03-22 fundamentals'
msr_psted = utils.read_msr(folder+'/3 sted psf with psted optics. hwp 38.5-128.5-5.msr')

# %%
channels = np.hstack([[4], np.arange(7, 25, 1)])
hwp_angles = np.arange(38.5, 129, 5)

channels, hwp_angles = channels[::2], hwp_angles[::2]

fig, ax = plt.subplots(2, 5, figsize=(linewidth, figheight),
    gridspec_kw=dict(hspace=.4), dpi=300)
ax = ax.flatten()
for i in range(len(channels)):
    ax[i].imshow(msr_psted[f'beads_STED_align {{{channels[i]}}}'][0])
    ax[i].axis('off')
    if i == 0:
        ax[i].set(title='HWP = 38.5°')
    else:
        ax[i].set(title=f'{hwp_angles[i]}°')

fig.savefig('../figures_generated/psted_psfs.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_psfs.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()