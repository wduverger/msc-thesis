# %%
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

import utils

# %%
files_apd1 = [
    '21-03-29 - 1c apd1 sensitivity - r3.msr',
    '21-03-29 - 1d apd1 sensitivity - r4.msr',
    '21-03-29 - 1e apd1 sensitivity - r5.msr',
]

files_apd2 = [
    '21-04-01 - 1a apd2 pol sensitivity r2.msr',
    '21-04-01 - 1a apd2 pol sensitivity r3.msr',
    '21-04-01 - 1a apd2 pol sensitivity r4.msr',
    '21-04-01 - 1a apd2 pol sensitivity r5.msr',
]

images_apd1 = [utils.read_msr('../data/' + file) for file in files_apd1]
images_apd2 = [utils.read_msr('../data/' + file) for file in files_apd2]

# %%


def analyse(im):
    channel_num = np.arange(2, 12)
    data = np.array([im[f'640_conf_apd2 {{{i}}}'].sum() for i in channel_num])
    return data


def row_norm(a):
    b = np.copy(a)
    for i in range(b.shape[0]):
        b[i] /= b[i].mean()
    return b


data_apd1 = row_norm(np.array([analyse(im) for im in images_apd1]))
data_apd2 = row_norm(np.array([analyse(im) for im in images_apd2]))

y1 = data_apd1.mean(axis=0)
y1err = data_apd1.std(axis=0)
y2 = data_apd2.mean(axis=0)
y2err = data_apd2.std(axis=0)

pol_angle = np.arange(0, 181, 20)
def cos(x, a, b, c): return a + b*np.cos((x-c)*np.pi/90)


popt1, _ = scipy.optimize.curve_fit(cos, pol_angle, y1, sigma=y1err)
popt2, _ = scipy.optimize.curve_fit(cos, pol_angle, y2, sigma=y2err)

fig, ax = plt.subplots(1, 2, sharey=True)

ax[0].errorbar(pol_angle, y1, yerr=y1err, ls='', capsize=3)
ax[1].errorbar(pol_angle, y2, yerr=y2err, ls='', capsize=3)

ax[0].plot(np.linspace(0, 180), cos(np.linspace(0, 180), *popt1),
           label='APD1 (n=3)', color='C0')
ax[1].plot(np.linspace(0, 180), cos(np.linspace(0, 180), *popt2),
           label='APD2 (n=4)', color='C0')

ax[0].set(
    title='APD1 (n=3)',
    xlabel='Polarisation angle',
    ylabel='APD signal (au) (mean ± std)',
    xticks=np.arange(0, 181, 45),
    xlim=[-10, 190]
)
ax[1].set(
    title='APD2 (n=4)',
    xlabel='Polarisation angle',
    ylabel='APD signal (au) (mean ± std)',
    xticks=np.arange(0, 181, 45),
    xlim=[-10, 190]
)

ax[0].hlines(1, *ax[0].get_xlim(), ls=':', alpha=.3)
ax[1].hlines(1, *ax[1].get_xlim(), ls=':', alpha=.3)

fig.savefig('../figures_generated/apd_pol_sensitivity.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/apd_pol_sensitivity.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()
