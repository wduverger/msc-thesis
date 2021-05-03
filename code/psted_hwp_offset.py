# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

import utils

# %%
df640     = utils.read_power_data('../data/21-03-22 - 3a 640 10% linear 0-10-170 scan through polariser at 90 deg.csv')
df775_45  = utils.read_power_data('../data/21-03-22 - 3b 775 0.1% hwp 0-5-90 offset 45.csv')
df775_385 = utils.read_power_data('../data/21-03-22 - 3b 775 0.1% hwp 0-5-90 offset 38.5.csv')

# %%
cos = lambda x, a, b, c: a + b * np.cos(2*(x-c)*np.pi/180)

fig, ax = plt.subplots(1, figsize=(utils.figwidth, utils.figheight))

xfine = np.linspace(0,180)

# 640 (ref)
xf = np.arange(0,171,10)
t, m, s = utils.find_steps(df640.p.values, distance=400, height=1e-10)
yf = m[1::2]/m.max()
popt, pcov = scipy.optimize.curve_fit(cos, xf, yf, bounds=((0, 0, 0), (1,1,180)))
ax.plot(xf, yf, '.', color='C0')
ax.plot(xfine, cos(xfine, *popt), color='C0', label='640 nm (+0°)')

# 775 (45)
xf = np.arange(0,181,10)
t, m, s = utils.find_steps(df775_45.p.values, distance=1000, height=1e-11)
yf = m[1:20]/df775_45.p.max()
popt, _ = scipy.optimize.curve_fit(cos, xf, yf, bounds=((0, 0, 0), (1,1,180)))
ax.plot(xf, yf, '.', color='C1')
ax.plot(xfine, cos(xfine, *popt), color='C1', label='775 nm (+45°)')

# 775 (38.5)
xf = np.arange(0,181,10)
t, m, s = utils.find_steps(df775_385.p.values, distance=1000, height=1e-11)
yf = m[1:20]/m[1:20].max()
popt, pcov = scipy.optimize.curve_fit(cos, xf, yf, bounds=((0, 0, 0), (1,1,180)))
ax.plot(xf, yf, '.', color='C2')
ax.plot(xfine, cos(xfine, *popt), color='C2', label='775 nm (+38.5°)')

mmax = m[np.isfinite(m)][1:20].max()
mmin = m[np.isfinite(m)][1:20].min()
print((mmax, mmin))
print(f'Imax/Imin = {mmax/mmin}')
print(f'chi_I = {np.arctan2(mmin, mmax) * 180 / np.pi} deg')
print(f'chi_E = {np.arctan2(np.sqrt(mmin), np.sqrt(mmax)) * 180 / np.pi} deg')

ax.set(
    xlim=[-10,190],
    xticks=np.arange(0,181,30),
    xlabel='Polarisation angle',
    ylabel='Power after polariser (au)',
    ylim=[0,1.1]
)
ax.legend()

ax2 = ax.twiny()
ax2.set(
    xlim=ax.get_xlim(),
    xticks=np.arange(0,181,30),
    xticklabels=np.arange(0,91,15),
    xlabel='HWP angle'
)

fig.savefig('../figures_generated/psted_hwp_offset.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_hwp_offset.svg', bbox_inches='tight')