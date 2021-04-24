# %%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import utils

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

msr = utils.read_msr('../data/21-04-20 - 2b sted psfs.msr')

# %% plot PSFs

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

fig, ax = plt.subplots(2,5, figsize=(linewidth, figheight), dpi=150, gridspec_kw=dict(hspace=.3))
ax = ax.flatten()

for i in range(10):
    im = msr[f'beads_STED_align {{{channel_numbers[i*2]}}}']
    peakj, peaki = np.unravel_index(im.argmax(), im.shape)
    di = 20
    ax[i].imshow(im[peakj-di:peakj+di, peaki-di:peaki+di])
    ax[i].axis('off')
    ax[i].set_title(hwp_angles[i*2])
    utils.add_scalebar(ax[i], 100e-9/im.pixel_size_xy, size_vertical=.5)

fig.savefig('../figures_generated/psted_psfs.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_psfs.svg', bbox_inches='tight')

# %% read PSF data

# This data was generated using `psted_psfs.ijm`
fiji = pd.read_csv('../data/psted_psfs.csv')

# Manipulate dataframe
fiji['pol'] = (fiji.Slice - 1) * 20
fiji['Angle'] -= 90
fiji.loc[fiji.Ch == 1, 'wavelength'] = 775
fiji.loc[fiji.Ch == 2, 'wavelength'] = 640
fiji.loc[fiji.Ch == 3, 'wavelength'] = 561
fiji['ellipticity'] = np.arctan2(fiji.Major, fiji.Minor) * 180 / np.pi

fiji775 = fiji[(fiji.wavelength==775) & (fiji.Area > .06)]


# %% Plot psf orientation and power
f775pol = fiji775.groupby('pol')
angle_mean = f775pol.mean().Angle
angle_std = f775pol.std().Angle
angle_mean[angle_mean.index > 90] += 180

fig, ax = plt.subplots(1,2, figsize=(linewidth, figheight), dpi=200, sharex=True,
    gridspec_kw=dict(wspace=.3))
ax[0].errorbar(x=angle_mean.index, y=angle_mean, yerr=angle_std,
            capsize=3)
ax[0].set(
    title='PSF orientation',
    xlabel='Depletion polarisation (deg)',
    ylabel='Orientation of major axis (deg)',
    xticks=np.arange(0,181,30),
    yticks=np.arange(0,181,30)
)

ax[1].errorbar(x=angle_mean.index, y=f775pol.IntDen.mean(), yerr=f775pol.IntDen.std(),
            capsize=3)
ax[1].set(
    title='pSTED power',
    xlabel=ax[0].get_xlabel(),
    ylabel='Total intensity of PSF'
)

fig.savefig('../figures_generated/psted_psfs_orientation_and_power.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_psfs_orientation_and_power.svg', bbox_inches='tight')
# %% Read PSF tracks

def dist(xys):
    return (xys**2).sum(axis=1)

def tracks(df):
    frames = len(fiji.Slice.unique())

    def get_xys(i):
        xs = df[df.Slice==i].X.values
        ys = df[df.Slice==i].Y.values
        return xs, ys


    tracks = []
    for x, y in zip(*get_xys(1)): 
        if not 2.2 < x < 2.7: # Delete one track that only has a 775 signal
            tracks.append([np.array((x, y))])

    for i in range(1,frames):
        xs, ys = get_xys(i+1)
        xys = np.vstack([xs, ys]).T

        for t in range(len(tracks)):
            nn = np.argmin(dist(tracks[t][0] - xys))
        #     print(t, nn)
            tracks[t].append(xys[nn])

    return [np.array(t-t[0]) 
            for t in tracks]

t775 = np.array(tracks(fiji[fiji.wavelength==775])) *1e3
t561 = np.array(tracks(fiji[fiji.wavelength==561]))*1e3
t640 = np.array(tracks(fiji[fiji.wavelength==640]))*1e3

# for t in t775:
#     t = np.array(t)
#     plt.scatter(t[:, 0], t[:,1], color='r')
# for t in t561:
#     t = np.array(t)
#     plt.scatter(t[:, 0], t[:,1], color='b')
# for t in t640:
#     t = np.array(t)
#     plt.scatter(t[:, 0], t[:,1], color='g')

# plt.xlim([1300,1800])
# plt.ylim([0,1000])



# %% Plot PSF tracks

mids = (t640 + t561)/2
# mids -= mids[:, 0, :]
midx = mids[..., 0]
midy = mids[..., 1]

disp = (t775 - mids) 
# disp -= disp[:, 0, :]
dispx = disp[..., 0]
dispy = disp[..., 1]

fig, ax = plt.subplots(1, 2, figsize=(linewidth, figheight), dpi=200, sharex=True, sharey=True)
ax[0].errorbar(np.linspace(0,180,10), midx.mean(axis=0), midx.std(axis=0), 
    capsize=3, label='x')
ax[0].errorbar(np.linspace(0,180,10), midy.mean(axis=0), midy.std(axis=0),
    capsize=3, label='y')


ax[1].errorbar(np.linspace(0,180,10), dispx.mean(axis=0), dispx.std(axis=0),
    capsize=3, label='775 x')
ax[1].errorbar(np.linspace(0,180,10), dispy.mean(axis=0), dispy.std(axis=0), 
    capsize=3, label='775 y')




ax[0].legend()
ax[0].set(
    xlabel='Depletion polarisation (deg)',
    xticks=np.arange(0,181,30),
    ylabel='Displacement (nm)',
    title='Excitation PSFs'
)
ax[1].set(
    xlabel=ax[0].get_xlabel(),
    title='pSTED PSF (relative to excitation)'
)

fig.savefig('../figures_generated/psted_psfs_displacement.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_psfs_displacement.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()
