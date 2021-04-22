# %%

import matplotlib.pyplot as plt
import numpy as np

import utils

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

msr = utils.read_msr('../data/21-04-20 - 2b sted psfs.msr')

# %%
pol_angles = np.arange(0,181,10)
hwp_angles = 180 + 38.5 - .5 * pol_angles
channel_numbers = np.arange(8,27)

def rgb_combine(r=None, g=None, b=None):
    shape = (r if r is not None else (g if g is not None else b)).shape
    rgb = np.zeros((*shape, 3))
    if r is not None: rgb[..., 0] = r/r.max()
    if g is not None: rgb[..., 1] = g/g.max()
    if b is not None: rgb[..., 2] = b/b.max()
    return rgb

fig, ax = plt.subplots(1,9, figsize=(9,2.7), dpi=150)
ax = ax.flatten()

for i in range(9):
    ax[i].imshow(rgb_combine(
        # r=msr[f'beads_STED_align {{{channel_numbers[2*i]}}}'],
        # g=msr[f'beads_640_align {{{channel_numbers[2*i]}}}'],
        b=msr[f'beads_561_align {{{channel_numbers[2*i]}}}'],
    ))
    ax[i].axis('off')

fig.savefig('../figures_generated/psted_psfs.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_psfs.svg', bbox_inches='tight')

# %%
s640 = [msr[f'beads_640_align {{{channel_numbers[i]}}}'] for i in range(19)]
s561 = [msr[f'beads_561_align {{{channel_numbers[i]}}}'] for i in range(19)]
s775 = [msr[f'beads_STED_align {{{channel_numbers[i]}}}'] for i in range(19)]

s640 = np.squeeze(s640)
s561 = np.squeeze(s561)
s775 = np.squeeze(s775)

def peak_loc(stack):
    Z, Y, X = stack.shape
    results = np.zeros((Z, 2))
    for i in range(Z):
        results[i] = np.unravel_index(np.argmax(stack[i]), (Y, X))
    return results

mean_disp = (peak_loc(s561) + peak_loc(s640))/2
actual_disp = peak_loc(s775) - mean_disp

fig, ax = plt.subplots(1, figsize=(figwidth, figheight))
ax.plot(pol_angles, (actual_disp-actual_disp[0, :])*msr['beads_STED_align {8}'].pixel_size_xy/1e-9)
ax.set(
    xlabel='pSTED polarisation angle (deg)',
    ylabel='Displacement (nm)',
    xticks=np.arange(0,181,30)
)
ax.legend(['y', 'x'])

# %%

fig, ax = plt.subplots(1, figsize=(figwidth, figheight))
ax.plot(pol_angles, s775.max(axis=(1,2)))
ax.set(
    xlabel='pSTED polarisation angle (deg)',
    ylabel='Max power (au)',
    xticks=np.arange(0,181,30)
)


# %%
utils.shutdown_jvm()