# %%
import numpy as np
import matplotlib.pyplot as plt
import utils

# %%
ca = 1.41
cc = 1
ce = 1

f_pulse  = 40e6
H_pulse = 39e-3
P_avg = 1.2

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

print(f'Safe levels: {14.1/f_pulse/H_pulse * 100}%')

fig, ax = plt.subplots(figsize=(utils.figwidth, utils.figheight))

ax.plot(t, h_mpe, label='MPE')
ax.plot(t, h_actual, label='Exposure at 100% power')
ax.plot(t, h_actual*.0005/100, label='Exposure at .0005% power')
ax.legend()
ax.set(
    xscale='log',
    yscale='log',
    xlabel='Exposure time (s)',
    ylabel='Dose received (J/m²)'
)

# %%
fig.savefig('../figures_generated/laser_safety.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/laser_safety.svg', bbox_inches='tight')
# %%
