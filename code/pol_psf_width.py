# %%

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

linewidth = (210-50)*.03937
figwidth  = .5 * linewidth
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

# %%
f = lambda x, i: np.cos(x)**2 * np.exp( -i * np.sin(x)**2)
w = lambda x, i: np.abs(f(x, i) - .5)

def find_fwhm(i):
    return scipy.optimize.minimize(
        w, .1*np.pi, args=(i,), bounds=[(0,np.pi/4)]
    ).x * 2 * 180 / np.pi

xlist = np.linspace(-90, 90, 100)
ilist = np.linspace(0,10)

fig, ax = plt.subplots(1, 2, figsize=(linewidth, figheight))

ax[0].plot(xlist, f(xlist * np.pi/180, 0), label='no pSTED')
ax[0].plot(xlist, f(xlist * np.pi/180, 2), label='pSTED')
ax[0].hlines(.5, xlist[0], xlist[-1], alpha=.3, ls=':')
ax[0].plot([-45, 45], [.5, .5], '.', color='C0')

hwhm = find_fwhm(i=2) / 2
ax[0].plot([-hwhm, hwhm], [.5, .5], '.', color='C1')

ax[0].legend()
ax[0].set(
    xlabel='Excitation angle (deg)',
    ylabel='Emission intensity',
    xticks=np.arange(-90, 91, 15)
)

ax[1].plot(ilist, [find_fwhm(i) for i in ilist])
ax[1].plot(0, find_fwhm(i=0), '.', color='C0')
ax[1].plot(2, find_fwhm(i=2), '.', color='C1')
ax[1].set(
    xlabel='Depletion intensity (au)',
    ylabel='FWHM (degres)'
)

# %%
fig.savefig('../figures_generated/pol_psf_width.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/pol_psf_width.svg', bbox_inches='tight')