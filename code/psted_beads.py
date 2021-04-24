# %%
import utils
import matplotlib.pyplot as plt
import numpy as np

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

# # %%
# msrc = utils.read_msr('../data/21-03-23 - 1c circular excitation, scan sted power at different psted angles.msr')
# msrl = utils.read_msr('../data/21-03-23 - 2b at 1% sted power.msr')

# # %%
# fig, ax = plt.subplots(1,2, figsize=(linewidth, figheight), gridspec_kw=dict(wspace=.3))

# channel_numbers = [3, 6, 7, 8, 9]
# sted_pol_angles = np.arange(0, 181, 45)
# sted_power_axis = 0.1 * np.linspace(.055, 1.25, 13)

# for i in range(len(channel_numbers)):
#     im = msrc[f'640_conf_apd2 {{{channel_numbers[i]}}}']
#     profile = im.sum(axis=(1,2))
#     ax[0].plot(sted_power_axis[1:], profile[1:]/profile[1:].max(), label=f'{sted_pol_angles[i]}°')

# ax[0].set_xlabel('Depletion power (W)')
# ax[0].set_ylabel('Remaining intensity on APD2 (au)')
# ax[0].set_title('Circular excitation')

# channel_numbers = np.arange(11,16)
# sted_pol_angles = np.arange(0, 181, 45)
# sted_power_axis = 0.01 * np.linspace(.055, 1.25, 13)

# for i in range(len(channel_numbers)):
#     im = msrl[f'640_conf_apd2 {{{channel_numbers[i]}}}']
#     profile = im.sum(axis=(1,2))
#     ax[1].plot(sted_power_axis[1:], profile[1:]/profile.max(), label=sted_pol_angles[i])
# ax[0 ].legend(title='Depletion\npolarisation')
# ax[1].set_xlabel('Depletion power (W) \n TODO: correct for power nonlinearity')
# # ax[1].set_ylabel('Remaining intensity (normalised)')
# ax[1].set_title('Linear excitation')
# ax[1].set_ylabel('Remaining intensity on APD2 (au)')

# fig.savefig('../figures_generated/psted_beads.pdf', bbox_inches='tight')
# fig.savefig('../figures_generated/psted_beads.svg', bbox_inches='tight')

# %%
msrLE = [
    utils.read_msr(rf"G:\New_OutLab\JonasSted\D-disken\User data\Wouter\2021-04-20 psfs and psted bead controls\3a psted bead controls {i+1}.msr")
    for i in range(5)
]

qwp_angles = np.arange(128.5, 220, 10)
pol_angles = ((38.5-qwp_angles)*2%360).astype(int)
folder = r'G:\New_OutLab\JonasSted\D-disken\User data\Wouter\2021-04-21 psted beads and yersinia'
files = [folder + f'/1 bead circular excitation hwp {t} r2.msr' for t in qwp_angles]
msrsCE = [utils.read_msr(f) for f in files]

dataCE = pd.concat([pd.DataFrame(dict(
        qwp_angle = [qwp_angles[i]]*10,
        conf = msrsCE[i]['640_conf_apd2 {1}'].mean(axis=(1,2)),
        psted = msrsCE[i]['640_psted_apd2 {1}'].mean(axis=(1,2)),
        power = power_axis,
    )) for i, m in enumerate(msrsCE)])

# %% 
matLE = np.array([m['640_psted_apd2 {1}'].sum(axis=(2,3)) for m in msrLE])

fig, ax = plt.subplots(1, 2, figsize=(linewidth, figheight), dpi=200, gridspec_kw=dict(wspace=0))

im1 = ax[1].imshow((matLE).mean(axis=0)/matLE.mean(axis=0).max(), cmap='bwr', vmax=1)


ax[1].set(
    xlabel='Excitation polarisation (deg)',
    ylabel='Depletion power (W)',
    xticks=np.arange(9),
    xticklabels=np.linspace(0, 160, 9, dtype=int),
    yticks=np.arange(10),
    yticklabels=power_axis.round(3),
    title='Linear excitation',
)

matCE = dataCE.psted.values.reshape([10,10])[9:0:-1, :]

im0 = ax[0].imshow(matCE.T/matCE.max(), cmap='bwr', vmax=1)


ax[0].set(
    title='Circular excitation',
    ylabel='Depletion power (W)',
    xlabel='Depletion polarisation (deg)',
    xticks=np.arange(9),
    xticklabels=pol_angles[-1::-1],
    yticks=np.arange(10),
    yticklabels=power_axis.round(3),
)

# plt.colorbar(im0, ax=ax[0])
plt.colorbar(im1, ax=ax[1], label='Fluorescence intensity (au)')

fig.savefig('../figures_generated/psted_beads.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_beads.svg', bbox_inches='tight')
# %%
utils.shutdown_jvm()