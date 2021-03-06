# %%

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from scipy.special import lambertw
import utils

# %%
psf = lambda x, i: np.cos(x)**2 * np.exp( -i * np.sin(x)**2)
fwhm = lambda i: 2*np.arccos(np.sqrt(np.real(lambertw(i * np.exp(i) / 2) / i))) * 180 / np.pi

xx = np.linspace(-90, 90, 100)
ii = np.linspace(1e-6,10)  # 0 doesn't work in the lambertw function

fig, ax = plt.subplots(1, 2, figsize=(utils.linewidth, utils.figheight),
gridspec_kw=dict(wspace=.4))

ax[0].plot(xx, psf(xx * np.pi/180, i=0), label='conventional')
ax[0].plot(xx, psf(xx * np.pi/180, i=2), label='pSTED')
ax[0].hlines(.5, xx[0], xx[-1], alpha=.3, ls=':')
ax[0].plot([-45, 45], [.5, .5], '.', color='C0')
ax[0].plot([-fwhm(2)/2, fwhm(2)/2], [.5, .5], '.', color='C1')

ax[0].legend(loc='lower right')
ax[0].set(
    xlabel='Excitation angle (deg)',
    ylabel='Emission intensity (I₀)',
    xticks=np.arange(-90, 91, 30)
)

ax[1].plot(ii, fwhm(ii))
ax[1].plot(0, fwhm(1e-6), '.', color='C0')
ax[1].plot(2, fwhm(2), '.', color='C1')

ax[1].set(
    xlabel='Depletion intensity (au)',
    ylabel='FWHM (degres)'
)

# %%
fig.savefig('../figures_generated/pol_psf_width.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/pol_psf_width.svg', bbox_inches='tight')
# %%
