# %%
import numpy as np
import matplotlib.pyplot as plt

import utils

linewidth = (210-50)*.03937
figwidth  = linewidth
figheight = 4.8 / 6.4 * figwidth /4
plt.rcParams['font.size'] = '6'

# %% 
msrs_gaussian = [
    utils.read_msr('../data/21-04-20 - 1b r1.msr'),
    utils.read_msr('../data/21-04-20 - 1b r1.msr'),
    utils.read_msr('../data/21-04-20 - 1b r1.msr'),
    utils.read_msr('../data/21-04-20 - 1b r1.msr'),
    utils.read_msr('../data/21-04-20 - 1b r1.msr'),
]

msrs_donut = [    
    utils.read_msr('../data/21-03-26 - 1 without psted optics - r1.msr'),
    utils.read_msr('../data/21-03-26 - 1 without psted optics - r2.msr'),
    utils.read_msr('../data/21-03-26 - 1 without psted optics - r3.msr'),
    utils.read_msr('../data/21-03-26 - 1 without psted optics - r4.msr'),
    utils.read_msr('../data/21-03-26 - 1 without psted optics - r5.msr'),
]

# %% 
def rgb_combine(r=None, g=None, b=None):
    shape = (r if r is not None else (g if g is not None else b)).shape
    rgb = np.zeros((*shape, 3))
    if r is not None: rgb[..., 0] = r/r.max()
    if g is not None: rgb[..., 1] = g/g.max()
    if b is not None: rgb[..., 2] = b/b.max()
    return rgb

c561 = lambda msr: msr['beads_561_align {4}']
c640 = lambda msr: msr['beads_640_align {4}']
csted = lambda msr: msr['beads_STED_align {4}']

def plot_row(msrs, row):
    avg561 = np.mean(np.array([c561(m) for m in msrs]), axis=0)
    avg640 = np.mean(np.array([c640(m) for m in msrs]), axis=0)
    avgsted = np.mean(np.array([csted(m) for m in msrs]), axis=0)

    ax[row, 0].imshow(rgb_combine(b=avg561))
    ax[row, 1].imshow(rgb_combine(g=avg640))
    ax[row, 2].imshow(rgb_combine(r=avgsted))
    ax[row, 3].imshow(rgb_combine(r=avgsted, g=avg640, b=avg561))

    for a in ax[row, :]: 
        a.axis('off')
        utils.add_scalebar(
            a, 200e-9/c561(msrs[0]).pixel_size_xy, size_vertical=1)

fig, ax = plt.subplots(2, 4, figsize=(linewidth, figheight*2.6)
    ,gridspec_kw=dict(hspace=0.1, wspace=0))
plot_row(msrs_donut, 0)
plot_row(msrs_gaussian, 1)
            
ax[0, 0].set_title('561 nm')
ax[0, 1].set_title('640 nm')
ax[0, 2].set_title('775 nm')
ax[0, 3].set_title('combined')

fig.savefig('../figures_generated/laser_psfs.pdf')
fig.savefig('../figures_generated/laser_psfs.svg')

# %%
utils.shutdown_jvm()