# %%
import numpy as np
import matplotlib.pyplot as plt

import utils

linewidth = (210-50)*.03937
figwidth  = linewidth
figheight = 4.8 / 6.4 * figwidth /2
plt.rcParams['font.size'] = '6'

# %% 561 polarisation

df_linear = utils.read_power_data(
    r'../data/21-03-22 - 1h 561 50% linear 0-10-170 power after stationary polariser.csv'
)

df_circular = utils.read_power_data(
    r'../data/21-03-22 - 1d 561 circular power after rotating polariser.csv'
)

# %%

p_avg = df_circular.p.rolling(100).mean()/1e-6
# print('For 561 circular')
# print(f'{p_avg.max()*5=}')
# print(f'{p_avg.min()*5=}')
# print(f'{p_avg.min()/p_avg.mean()=}')

fig, ax = plt.subplots(1, 2, figsize=(figwidth, figheight), sharey=True)

ax[0].plot(df_linear.t, df_linear.p/1e-6,  alpha=.3)
ax[0].plot(df_linear.t, df_linear.p.rolling(100).mean()/1e-6, color='C0')
ax[0].set(
    xlabel='Measurement time (s)',
    ylabel='Transmitted power (μW)',
    title='561 nm: linearly polarised'
)

ax[1].plot(df_circular.t, df_circular.p*5/1e-6,  alpha=.3)
ax[1].plot(df_circular.t, df_circular.p.rolling(300).mean()*5/1e-6, color='C0')
ax[1].set(
    xlabel='Measurement time (s)\n TODO: mention multiplying these values by 5',
    ylim=[-.01, .29],
    title='Circularly polarised',
)

fig.savefig('../figures_generated/561 laser pol characteristics in sample.pdf', bbox_inches='tight')

# %% 640 linear at sample

df_linear = utils.read_power_data(
    r'../data/21-03-22 - 1g 640 10% linear 0-10-170 power after stationary polariser.csv'
)

df_circular = utils.read_power_data(
    r'../data/21-03-22 - 1e 640 circular power after rotating polariser.csv'
)

# %%

p_avg = df_circular.p.rolling(100).mean()/1e-6
mask = (df_circular.t > 10) & (df_circular.t < 50)
# print('For 640 circular')
# print(f'{p_avg[mask].max()=}')
# print(f'{p_avg[mask].min()=}')
# print(f'{p_avg[mask].min()/p_avg[mask].max()=}')

fig, ax = plt.subplots(1, 2, figsize=(figwidth, figheight), sharey=True)

ax[0].plot(df_linear.t, df_linear.p/1e-6, alpha=.3)
ax[0].plot(df_linear.t, df_linear.p.rolling(100).mean()/1e-6, color='C0')
ax[0].set(
    title='640 nm: linearly polarised',
    xlim=[0,80],
    xlabel='Measurement time (s)',
    ylabel='Laser power (μW)',
)

ax[1].plot(df_circular.t, df_circular.p/1e-6,  alpha=.3)
ax[1].plot(df_circular.t.rolling(500).mean(), df_circular.p.rolling(500).mean()/1e-6, color='C0')
ax[1].set(
    xlabel='Measurement time (s)\nTODO: shouldn\'t these y values be lower?',
    # ylim=[-.01, .29],
    title='Circularly polarised',
    xlim=[10,60]
)


fig.savefig('../figures_generated/640 laser pol characteristics in sample.pdf', bbox_inches='tight')

# %% 775 nm 

df = utils.read_power_data('../data/21-03-22 - 1f 775 circular power after rotating polariser.csv')

p_avg = df.p.rolling(100).mean()/1e-6
mask = (df.t < 12)
# print('For 775 circular')
# print(f'{p_avg[mask].max()=}')
# print(f'{p_avg[mask].min()=}')
# print(f'{p_avg[mask].min()/p_avg[mask].max()=}')

fig, ax = plt.subplots(1, figsize=(figwidth/2, figheight))

ax.plot(df.t, df.p/1e-6, alpha=.3)
ax.plot(df.t.rolling(100).mean(), df.p.rolling(100).mean()/1e-6, color='C0')
ax.set(
    title='775 nm: circularly polarised',
    xlim=[0,12],
    xlabel='Measurement time (s)',
    ylabel='Laser power (μW)',
)

fig.savefig('../figures_generated/775 laser pol characteristics in sample (donut beam, no psted optics).pdf', bbox_inches='tight')
