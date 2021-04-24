# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import utils

folder = r'G:\New_OutLab\JonasSted\D-disken\User data\Wouter\2021-04-23 psted hires scans'

msr2 = utils.read_msr(folder + '/1 fov2.msr')
conf2 = msr2['640_conf_apd2 {2}']
sted2 = msr2['640_psted_apd2 {2}']

msr3 = utils.read_msr(folder + '/1 fov3.msr')
conf3 = msr3['640_conf_apd2 {2}']
sted3 = msr3['640_psted_apd2 {2}']

msr4 = utils.read_msr(folder + '/1 fov4.msr')
conf4 = msr4['640_conf_apd2 {2}']
sted4 = msr4['640_psted_apd2 {2}']

# %%

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

profile_multiplier = 1e4
profile = lambda im, x0, y0, d: im[:, y0:y0+d, x0:x0+d].mean(axis=(1,2)) * profile_multiplier
pol = lambda hwp: ((218.5-hwp)*2)

fig, ax = plt.subplots(2, 3, figsize=(linewidth, figheight))
ax = ax.T

x1,y1,d1 = 212, 122, 30
hwp = np.arange(128.5, 158.6, 2.5)
pc = profile(conf2, x1, y1, d1)
ps = profile(sted2, x1, y1, d1)

ax[0, 0].imshow(conf2[0])
ax[0, 0].add_patch(Rectangle((x1, y1), d1, d1, fill=None, color='red'))
ax[0, 1].plot(pol(hwp), pc-pc.mean())
ax[0, 1].plot(pol(hwp), ps-ps.mean())
ax[0, 1].set(xticks=pol(hwp)[::4])

x2, y2, d2 = 172, 98, 20
hwp = np.arange(163.5, 128.4, -2.5)
pc = profile(conf3, x2, y2, d2)
ps = profile(sted3, x2, y2, d2)

ax[1, 0].imshow(conf3[0])
ax[1, 0].add_patch(Rectangle((x2, y2), d2, d2, fill=None, color='red'))
ax[1, 1].plot(pol(hwp), pc-pc.mean())
ax[1, 1].plot(pol(hwp), ps-ps.mean())
ax[1, 1].set(xticks=pol(hwp)[::4])

hwp = np.arange(168.5, 143.4, -2.5)
pc = conf4.mean(axis=(1,2))
ps = sted4.mean(axis=(1,2))

_, J, I = conf4.shape
ax[2, 0].imshow(conf4[0])
ax[2, 0].add_patch(Rectangle((0, 0), I-2, J-2, fill=None, color='red'))
ax[2, 1].plot(pol(hwp), (pc-pc.mean())*profile_multiplier)
ax[2, 1].plot(pol(hwp), (ps-ps.mean())*profile_multiplier)
ax[2, 1].set(xticks=pol(hwp)[::4])

for i, m in enumerate([conf2, conf3, conf4]):
    ax[i, 0].axis('off')
    utils.add_scalebar(ax[i, 0], 2e-6/m.pixel_size_xy)
    
    ax[i, 1].set(
        xlabel='Depletion polarisation (deg)',
        ylabel='Intensity (norm)' if i==0 else ''
    )

fig.savefig('../figures_generated/psted_scans.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_scans.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()