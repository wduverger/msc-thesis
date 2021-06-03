# %%
import numpy as np
import matplotlib.pyplot as plt

import utils

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
utils.shutdown_jvm()

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

    for i, a in enumerate(ax[row, :]): 
        a.axis('off')
        add_label = i == 3 and row==0
        utils.add_scalebar(
            a, 
            500e-9/c561(msrs[0]).pixel_size_xy, 
            '500 nm' if add_label else '', 
            size_vertical=1
        )

fig, ax = plt.subplots(2, 4,figsize=(utils.linewidth, 1.3*utils.figheight))
plot_row(msrs_donut, 0)
plot_row(msrs_gaussian, 1)
            
ax[0, 0].set_title('561 nm')
ax[0, 1].set_title('640 nm')
ax[0, 2].set_title('775 nm')
ax[0, 3].set_title('combined')

fig.savefig('../figures_generated/laser_psfs.pdf')
fig.savefig('../figures_generated/laser_psfs.svg')

# %%