#%%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import utils

# %%
data = pd.read_csv(
    '../data/21-04-14 Laser power data from Jason.csv',
    sep=';', decimal=','
)

fig, ax = plt.subplots(1, 2)

sources = ['561', '640', '775 @1,2W']
norms = [1, 1, 1e-3]
labels = ['561 nm', '640 nm', '775 nm, 1.2 W (x$ 10^{-3}$)']

# Plot 0: low xmax
xmax = 5
for s, n, l in zip(sources, norms, labels):
    d = data[(data.source == s) & (data['power setting (%)'] <= xmax)]
    x = d['power setting (%)']
    y = d['power measured (μW)']
    ax[0].plot(x, y*n, '.-', label=l, ms=3)

ax[0].legend(title='Laser source')
ax[0].set(
    xlabel='Power setting (%)',
    ylabel='Power (μW)',
    title='Low powers'
)

# PLot 1: whole x
for s, n, l in zip(sources, norms, labels):
    d = data[(data.source == s)]
    x = d['power setting (%)']
    y = d['power measured (μW)']
    ax[1].plot(x, y*n, '.-', label=l, ms=3)

ax[1].set(
    xlabel='Power setting (%)',
    title='High powers'
)

# %%

fig.savefig('../figures_generated/laser_power.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/laser_power.svg', bbox_inches='tight')
# %%
