# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
linewidth = (210-50)*.03937
figwidth  = .5 * linewidth
figheight = 4.8 / 6.4 * figwidth

# %%
ca = 1.41
cc = 1
ce = 1

f_pulse  = 40e6
H_pulse = 39e-3

t = np.logspace(-7, 3, num=100, dtype=np.float)

#%%
h_actual = np.floor(t * f_pulse) * H_pulse

h_mpe_short = 5e-3 * ca * ce
h_mpe_mid   = 18 * t**.75 * ca * ce
h_mpe_long  = 10 * t * ca * cc
h_mpe = np.where(
    t>10, h_mpe_long,
    np.where(
        t>18e-6, h_mpe_mid,
        h_mpe_short
    )
)

power = .5e-5

plt.rcParams['font.size'] = '6'
fig, ax = plt.subplots(1,1, figsize=(figwidth, figheight), dpi=300)

ax.plot(t, h_mpe, label='MPE')
ax.plot(t, h_actual, label='100% power')
ax.plot(t, h_actual*power, label=f'{power*100:.4f}% power')
ax.legend()
ax.set(
    xscale='log',
    yscale='log',
    xlabel='Exposure time ( $s$ )',
    ylabel='Dose received ( $J/m^2$ )'
)

# %%
fig.savefig('../figures_generated/laser_safety.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/laser_safety.svg', bbox_inches='tight')
# %%
