# %%
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

import utils

# %% data

with open('../data/beampol_calib.json', 'r') as file:
    calib_json = json.load(file)

# %% plots

calib_old_axis = np.arange(0, 176, 5)

fig, (ax0, ax1) = plt.subplots(1,2, sharey=True, sharex=True)

φ2 = np.array(calib_json['calibrations']
              ['Polarizer_561']['linear']['l2'])
φ4 = np.array(calib_json['calibrations']
              ['Polarizer_561']['linear']['l4'])

ax0.plot(calib_old_axis, φ2, label='λ/2')
ax0.plot(calib_old_axis, φ4, label='λ/4')

φ2 = np.array(calib_json['calibrations']
              ['Polarizer_640']['linear']['l2'])
φ4 = np.array(calib_json['calibrations']
              ['Polarizer_640']['linear']['l4'])
              
ax1.plot(calib_old_axis, φ2)
ax1.plot(calib_old_axis, φ4)

ax0.legend()

ax0.set(
    title='561 nm',
    ylabel='Waveplate position (deg)',
    xlabel='Polarisation in sample plane (deg)',
    xticks=np.arange(0,181,45),
    xlim=[-10,190],
    yticks=np.arange(0,181,45),
    ylim=[-10,190],
)

ax1.set(
    title='640 nm',
    xlabel=ax0.get_xlabel()
)

fig.savefig('../figures_generated/excitation_waveplate_calibrations.pdf',
            bbox_inches='tight')
fig.savefig('../figures_generated/excitation_waveplate_calibrations.svg',
            bbox_inches='tight')
# %%
