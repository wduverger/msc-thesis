# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import utils

linewidth = (210-50)*.03937
figwidth  = linewidth
figheight = 4.8 / 6.4 * figwidth /2
plt.rcParams['font.size'] = '6'

# %% data

l561 = utils.read_power_data(
    r'../data/21-03-22 - 1h 561 50% linear 0-10-170 power after stationary polariser.csv'
)
c561 = utils.read_power_data(
    r'../data/21-04-08 - 1b 561 lc 100%.csv'
)
l640 = utils.read_power_data(
    r'../data/21-03-22 - 1g 640 10% linear 0-10-170 power after stationary polariser.csv'
)
c640 = utils.read_power_data(
    r'../data/21-04-08 - 1a 640 rc 30%.csv'
)
c775 = utils.read_power_data(
    r'../data/21-04-08 - 1d 665 0.4%.csv'
)

# %% plotting

avg_p = lambda x: x.p.rolling(100).mean()
micro = 1e-6

fig, ax = plt.subplots(
    3, 2, figsize=(figwidth, 3*figheight),
    gridspec_kw=dict(hspace=.4)
)

ax[0, 0].plot(c561.t, c561.p/micro, alpha=.3)
ax[0, 0].plot(c561.t, avg_p(c561)/micro, color='C0')
ax[0, 0].set(
    ylabel='Transmitted power (μW)',
    title='561 nm (circular, 100%)',
    xlabel='Measurement time (s)'
)

ax[0, 1].plot(l561.t, l561.p/micro, alpha=.3)
ax[0, 1].plot(l561.t, avg_p(l561)/micro, color='C0')
ax[0, 1].set(
    title='561 nm (linear, 50%)',
    xlabel='Measurement time (s)'
)

# t, m, s, cl, cr = find_steps(c640.p.values, distance=2500, calc_margin=.3)
# ax[1, 0].step(c640.t[t+200], m/micro, where='post', color='C1')
ax[1, 0].plot(c640.t, c640.p/micro, alpha=.3, color='C0')
ax[1, 0].plot(c640.t, avg_p(c640)/micro, color='C0')
ax[1, 0].set(
    ylabel='Transmitted power (μW)',
    title='640 nm (circular, 30%)',
    xlabel='Measurement time (s)'
)

ax[1, 1].plot(l640.t, l640.p/micro, alpha=.3)
ax[1, 1].plot(l640.t, avg_p(l640)/micro, color='C0')
ax[1, 1].set(
    title='640 nm (linear, 10%)',
    xlabel='Measurement time (s)',
    xlim=[0,80]
)

# t, m, s, cl, cr = find_steps(c775.p.values, distance=2300, calc_margin=.45)
# ax[2, 0].step(c775.t[t], m/micro, where='post', color='C1')
ax[2, 0].plot(c775.t, c775.p/micro, alpha=.3, color='C0')
ax[2, 0].plot(c775.t, avg_p(c775)/micro, color='C0')
ax[2, 0].set(
    ylabel='Transmitted power (μW)',
    title='775 nm (circular, 0.4%)',
    xlabel='Measurement time (s)'
)

ax[2, 1].axis('off')

#%% analysis

data = pd.DataFrame([
    dict(
        source='561c',
        min=avg_p(c561).min(),
        max=avg_p(c561).max(),
    ),
    dict(
        source='640c',
        min=avg_p(c640).min(),
        max=avg_p(c640).max(),
    ),
    dict(
        source='775c',
        min=avg_p(c775).min(),
        max=avg_p(c775).max(),
    ),
    dict(
        source='561l',
        min=avg_p(l561).min(),
        max=avg_p(l561).max(),
    ),
    dict(
        source='640l',
        min=avg_p(l640[l640.p>.03e-6]).min(),
        max=avg_p(l640[l640.p<.3e-6]).max(),
    ),
])

data['max/min'] = data['max']/data['min']
data['chi'] = np.arctan2(data['min'], data['max']) * 180 / np.pi

print('Laser polarisation estimates:')
print(data)

# %% saving figures

fig.savefig('../figures_generated/laser_polarisation.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/laser_polarisation.svg', bbox_inches='tight')