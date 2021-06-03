# %%

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import utils

msr2 = utils.read_msr('../data/21-04-23 - 1 fov2.msr')
conf2 = msr2['640_conf_apd2 {2}']
sted2 = msr2['640_psted_apd2 {2}']

msr3 = utils.read_msr('../data/21-04-23 - 1 fov3.msr')
conf3 = msr3['640_conf_apd2 {2}']
sted3 = msr3['640_psted_apd2 {2}']

# msr4 = utils.read_msr('../data/21-04-23 - 1 fov4.msr')
# conf4 = msr4['640_conf_apd2 {2}']
# sted4 = msr4['640_psted_apd2 {2}']

msr5 = utils.read_msr('../data/21-04-23 - 1 fov5.msr')
conf5 = msr5['640_conf_apd2 {2}']
sted5 = msr5['640_psted_apd2 {2}']

utils.shutdown_jvm()

# %%

profile_multiplier = 1e4
profile = lambda im, x0, y0, d: im[:, y0:y0+d, x0:x0+d].mean(axis=(1,2)) * profile_multiplier
pol = lambda hwp: ((218.5-hwp)*2)
norm = lambda p: (p-p.min())/(p.max()-p.min())

fig, ax = plt.subplots(
    2, 3, dpi=150, 
    figsize=(utils.linewidth, 2*utils.figheight),
    gridspec_kw=dict(wspace=.3),
    sharey='row'
)
ax=ax.T

figb, axb = plt.subplots(
    2, 2, dpi=150, 
    figsize=(utils.linewidth, 2*utils.figheight),
    gridspec_kw=dict(wspace=.3)
)

x1,y1,d1 = 212, 122, 30
hwp = np.arange(128.5, 158.6, 2.5)
pc = profile(conf2, x1, y1, d1)
ps = profile(sted2, x1, y1, d1)

ax[0, 0].imshow(conf2[0])
ax[0, 0].add_patch(Rectangle((x1, y1), d1, d1, fill=None, color='red'))
ax[0, 1].plot(pol(hwp), norm(pc))
ax[0, 1].plot(pol(hwp), norm(ps))
ax[0, 1].set(
    xlim=ax[0,1].get_xlim()[::-1],
    xticks=pol(hwp)[::4]
)

axb[0, 0].imshow(conf2[0])
axb[0, 0].add_patch(Rectangle((x1, y1), d1, d1, fill=None, color='red'))
axb[0, 1].plot(pol(hwp), norm(pc))
axb[0, 1].plot(pol(hwp), norm(ps))
axb[0, 1].set(
    xlim=axb[0,1].get_xlim()[::-1],
    xticks=pol(hwp)[::4]
)

x2, y2, d2 = 172, 98, 20
hwp = np.arange(163.5, 128.4, -2.5)
pc = profile(conf3, x2, y2, d2)
ps = profile(sted3, x2, y2, d2)

ax[1, 0].imshow(conf3[0])
ax[1, 0].add_patch(Rectangle((x2, y2), d2, d2, fill=None, color='red'))
ax[1, 1].plot(pol(hwp), norm(pc))
ax[1, 1].plot(pol(hwp), norm(ps))
ax[1, 1].set(xticks=pol(hwp)[::4])

# hwp = np.arange(168.5, 143.4, -2.5)
# pc = conf4.mean(axis=(1,2))
# ps = sted4.mean(axis=(1,2))

# _, J, I = conf4.shape
# ax[2, 0].imshow(conf4[0])
# ax[2, 0].add_patch(Rectangle((0, 0), I-1, J-1, fill=None, color='red'))
# ax[2, 1].plot(pol(hwp), (pc-pc.mean())*profile_multiplier)
# ax[2, 1].plot(pol(hwp), (ps-ps.mean())*profile_multiplier)
# ax[2, 1].set(xticks=pol(hwp)[::4])

x3, y3, d3 = 114, 272, 30
hwp = np.arange(218.5, 128.4, -5)
pc = profile(conf5, x3, y3, d3)
ps = profile(sted5, x3, y3, d3)

ax[2, 0].imshow(conf5[0])
ax[2, 0].add_patch(Rectangle((x3, y3), d3, d3, fill=None, color='red'))
ax[2, 1].plot(pol(hwp), norm(pc))
ax[2, 1].plot(pol(hwp), norm(ps))
ax[2, 1].set(xticks=pol(hwp)[::4])

axb[1, 0].imshow(conf5[0])
axb[1, 0].add_patch(Rectangle((x3, y3), d3, d3, fill=None, color='red'))
axb[1, 1].plot(pol(hwp), norm(pc))
axb[1, 1].plot(pol(hwp), norm(ps))
axb[1, 1].set(xticks=pol(hwp)[::4])

for i, m in enumerate([conf2, conf3, conf5]):
    ax[i, 0].axis('off')
    utils.add_scalebar(ax[i, 0], 10e-6/m.pixel_size_xy, '10 μm' if i == 2 else '')
    
    ax[i, 1].set(
        xlabel='Depletion polarisation (deg)',
        ylabel='Intensity (au)' if i==0 else ''
    )

    if i == 2:
        ax[i, 1].legend(['Confocal', 'pSTED'], loc='upper right')
    
for i, m in enumerate([conf2, conf5]):
    axb[i, 0].axis('off')
    utils.add_scalebar(axb[i, 0], 2e-6/m.pixel_size_xy)
    
    axb[i, 1].set(
        xlabel='Depletion polarisation (deg)' if i==1 else '',
        ylabel='Intensity (au)'
    )

    if i == 0:
        axb[i, 1].legend(['Confocal', 'pSTED'], loc='upper right')

fig.savefig('../figures_generated/psted_scans.pdf', bbox_inches='tight')
figb.savefig('../figures_generated/psted_scans_short.svg', bbox_inches='tight')

# %%