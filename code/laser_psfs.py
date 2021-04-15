# %%
import numpy as np
import matplotlib.pyplot as plt

import utils

linewidth = (210-50)*.03937
figwidth  = linewidth
figheight = 4.8 / 6.4 * figwidth /4
plt.rcParams['font.size'] = '6'

# %% 
images = utils.read_msr('../data/21-03-22 - 2 sted psf without psted components.msr')
psf_561_donut = images['beads_561_align {4}'][0]
psf_640_donut = images['beads_640_align {4}'][0]
psf_775_donut = images['beads_STED_align {4}'][0]
psf_561_gaussian = images['beads_STED_align {7}'][0]
psf_640_gaussian = images['beads_640_align {7}'][0]
psf_775_gaussian = images['beads_561_align {7}'][0]

# %% donut
def rgb_combine(r=None, g=None, b=None):
    shape = (r if r is not None else (g if g is not None else b)).shape
    rgb = np.zeros((*shape, 3))
    if r is not None: rgb[..., 0] = r/r.max()
    if g is not None: rgb[..., 1] = g/g.max()
    if b is not None: rgb[..., 2] = b/b.max()
    return rgb

fig, ax = plt.subplots(2, 4, figsize=(linewidth, figheight*2.6))#, gridspec_kw=dict(hspace=))
ax[0, 0].imshow(rgb_combine(b=psf_561_donut))
ax[0, 1].imshow(rgb_combine(g=psf_640_donut))
ax[0, 2].imshow(rgb_combine(r=psf_775_donut))
ax[0, 3].imshow(rgb_combine(b=psf_561_donut, g=psf_640_donut, r=psf_775_donut))

ax[1, 0].imshow(rgb_combine(b=psf_561_gaussian))
ax[1, 1].imshow(rgb_combine(g=psf_640_gaussian))
ax[1, 2].imshow(rgb_combine(r=psf_775_gaussian))
ax[1, 3].imshow(rgb_combine(b=psf_561_gaussian, g=psf_640_gaussian, r=psf_775_gaussian))


ax[0, 0].set_title('561 nm')
ax[0, 1].set_title('640 nm')
ax[0, 2].set_title('775 nm (donut)')
for a in ax[0, :]: 
    a.axis('off')
    utils.add_scalebar(
        a, 200e-9/psf_775_donut.pixel_size_xy, size_vertical=1)

ax[1, 0].set_title('561 nm')
ax[1, 1].set_title('640 nm')
ax[1, 2].set_title('775 nm (Gaussian)')
for a in ax[1, :]: 
    a.axis('off')
    utils.add_scalebar(
        a, 200e-9/psf_775_gaussian.pixel_size_xy, size_vertical=1)

fig.savefig('../figures_generated/laser_psfs.pdf')
fig.savefig('../figures_generated/laser_psfs.svg')

# %%
utils.shutdown_jvm()