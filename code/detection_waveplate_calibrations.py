# %%
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

import utils

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

# %% data

with open('../data/beampol_calib.json', 'r') as file:
    calib_json = json.load(file)


msr_old = utils.read_msr(
    '../data/21-03-22 - 5b detector waveplates old abberior calibration.msr')
msr_new = utils.read_msr(
    '../data/21-03-22 - 5a detector waveplates my calibration - rerun.msr')

# %%
calib_old_axis = np.arange(0, 180, 5)
fine_axis = np.linspace(0, 180)
φ2 = np.array(calib_json['calibrations']
              ['Polarizer_Detection']['linear']['l2'])
φ4 = np.array(calib_json['calibrations']
              ['Polarizer_Detection']['linear']['l4'])
φ2[φ2 > 200] -= 360

fig, ax = plt.subplots(
    2, 2, sharex=True, sharey='row',
    figsize=(linewidth, 1.5*figheight),
    gridspec_kw=dict(wspace=0.1)
)

# Old calib
ax[0, 0].plot(calib_old_axis, φ2)
ax[0, 0].plot(calib_old_axis, φ4)
ax[0, 0].set(
    title='Default calibration',
    ylabel='Waveplate angle',
    yticks=np.arange(0, 230, 45),
    ylim=[-20, 245]
)

# New calib
ax[0, 1].plot(fine_axis, fine_axis/2, label='HWP')
ax[0, 1].plot(fine_axis, fine_axis*0+50, label='QWP')
ax[0, 1].legend()
ax[0, 1].set_title('New calibration')


# Intensity plots
x_axis = np.arange(0, 171, 10)
for i in range(4):
    ax[1, 0].plot(x_axis, msr_old[f'apd2 {{{i}}}'].sum(axis=(1, 2)), '.-')
    ax[1, 1].plot(x_axis, msr_new[f'apd2 {{{i}}}'].sum(
        axis=(1, 2)), '.-', label=f'{i*45:d}°')

ax[1, 0].set(
    xlabel='Rotation angle',
    xticks=np.arange(0, 181, 45),
    ylabel='Intensity after P2 (au)'
)
ax[1, 1].legend(title='P2 angle', loc='upper right')
ax[1, 1].set(
    xlabel='Rotation angle'
)

fig.savefig('../figures/detection_waveplate_calibrations.pdf',
            bbox_inches='tight')
fig.savefig('../figures/detection_waveplate_calibrations.svg',
            bbox_inches='tight')

# %%
utils.shutdown_jvm()
