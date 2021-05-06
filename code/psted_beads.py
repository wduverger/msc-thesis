# %%
import utils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %% data ingestion
power_axis = 0.1 * np.linspace(.055, 1.25, 10)
pol_angles_LE = np.arange(0, 161, 20)
msrLE = [
    utils.read_msr(f"../data/21-04-20 - 3a psted bead controls {i+1}.msr")
    for i in range(5)
]

# MSR CE #1
hwp_angles1 = np.arange(128.5, 220, 10)
pol_angles1 = ((38.5-hwp_angles1)*2%360).astype(int)
files = [f'../data/21-04-21 - 1 bead circular excitation hwp {t} r2.msr' for t in hwp_angles1]
msrsCE1 = [utils.read_msr(f) for f in files]

# msrCE #2
channels = np.arange(1,11)
hwp2 = np.arange(218.5,138.4, -10)
msrCE2 = utils.read_msr(
    '../data/21-04-30 - repeat1.msr'
)
utils.shutdown_jvm()

# %% data analysis

matLE = np.array([m['640_psted_apd2 {1}'].sum(axis=(2,3)) for m in msrLE])
matLE = matLE.mean(axis=0)

dataCE1 = pd.concat([pd.DataFrame(dict(
        qwp_angle = [hwp_angles1[i]]*10,
        conf = msrsCE1[i]['640_conf_apd2 {1}'].mean(axis=(1,2)),
        psted = msrsCE1[i]['640_psted_apd2 {1}'].mean(axis=(1,2)),
        power = power_axis,
    )) for i, m in enumerate(msrsCE1)])
matCE1 = dataCE1.psted.values.reshape([10,10])[9:0:-1, :].T

matCE1 = np.zeros((len(power_axis), len(hwp_angles1)-1))
for i in range(1, len(hwp_angles1)): # Don't take the first data point (pol at 180 deg), since the other data don't have this
    conf = msrsCE1[i]['640_conf_apd2 {1}'].mean(axis=(1,2))
    psted = msrsCE1[i]['640_psted_apd2 {1}'].mean(axis=(1,2))
    matCE1[:, i-1] = psted
matCE1 = matCE1[:, ::-1]  # Reverse pol axis

matCE2 = np.zeros((len(power_axis), len(hwp2)))
for i, c in enumerate(channels):
    conf = msrCE2[f'640_conf_apd2 {{{c}}}'].mean(axis=(1,2))
    psted = msrCE2[f'640_psted_apd2 {{{c}}}'].mean(axis=(1,2))
    matCE2[i, :] = psted
    

# %% data vis

norm = lambda x: x/x.max()
vmin=.3

fig, ax = plt.subplots(1, 2, figsize=(utils.linewidth, utils.figheight), 
    gridspec_kw=dict(wspace=-.4), sharey=True, dpi=200)

im0 = ax[0].imshow(norm(matLE), cmap='bwr', vmax=1, vmin=vmin)

xticks = np.arange(0,9,2)
xticklabels = np.linspace(0, 160, 5, dtype=int)

ax[0].set(
    xlabel='Excitation pol (deg)',
    ylabel='Depletion power (W)',
    xticks=xticks,
    xticklabels=xticklabels,
    yticks=np.arange(10),
    yticklabels=power_axis.round(3),
    title='Linear',
)


im1 = ax[1].imshow((norm(matCE1)+norm(matCE2))/2, cmap='bwr', vmax=1, vmin=vmin)

ax[1].set(
    title='Circular 1',
    xlabel='Depletion pol (deg)',
    xticks=np.arange(0,9,2),
    xticklabels=pol_angles1[-1::-2],
    yticks=np.arange(10),
    yticklabels=power_axis.round(3),
)

plt.colorbar(mappable=im1, ax=ax[1], label='Fraction of remaining\nfluorescence intensity')

fig.savefig('../figures_generated/psted_beads.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_beads.svg', bbox_inches='tight')
# %%