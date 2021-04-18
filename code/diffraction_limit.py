# %%

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1


linewidth = (210-50)*.03937
figwidth  = linewidth / 2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

conf_psf = lambda x: 4*(j1(x)/x) ** 2

q = np.linspace(-1,3, 200)
C = np.pi * 1.22
x = C * q

def plot(distance_q, axis):
    sep_x = -distance_q * C
    axis.plot(q, conf_psf(x), color='C0', ls=':', lw=.5)
    axis.plot(q, conf_psf(x+sep_x), color='C0', ls=':', lw=.5)
    axis.plot(q, conf_psf(x)+conf_psf(x+sep_x) , color='C0')

fig, ax = plt.subplots(1, 4, sharey=True, figsize=(linewidth, figheight*.66))
plot(.5, ax[0])
ax[0].set(
    title='Below limit',
    xlabel='Distance (1.22 λ / NA)',
    ylabel='Intensity ($I_0$)',
    ylim=[-.05, 1.25],
    xticks=np.arange(-1, 3.2, 1)
)
plot(1, ax[2])
ax[2].set(
    title='Raileygh criterion',
    xlabel='Distance (1.22 λ / NA)',
    xticks=np.arange(-1, 3.2, 1)
)
plot(.47/.61, ax[1])
ax[1].set(
    title='Sparrow criterion',
    xlabel='Distance (1.22 λ / NA)',
    xticks=np.arange(-1, 3.2, 1)
)
plot(1.5, ax[3])
ax[3].set(
    title='Above limit',
    xlabel='Distance (1.22 λ / NA)',
    xticks=np.arange(-1, 3.2, 1)
)

fig.savefig('../figures_generated/diffraction_limit.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/diffraction_limit.svg', bbox_inches='tight')

# %%
