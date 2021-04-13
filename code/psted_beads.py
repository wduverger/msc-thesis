# %%
import utils
import matplotlib.pyplot as plt
import numpy as np

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

# %%
msrc = utils.read_msr('../data/21-03-23 - 1c circular excitation, scan sted power at different psted angles.msr')
msrl = utils.read_msr('../data/21-03-23 - 2b at 1% sted power.msr')

# %%
fig, ax = plt.subplots(1,2, figsize=(linewidth, figheight), gridspec_kw=dict(wspace=.3))

channel_numbers = [3, 6, 7, 8, 9]
sted_pol_angles = np.arange(0, 181, 45)
sted_power_axis = 0.1 * np.linspace(.055, 1.25, 13)

for i in range(len(channel_numbers)):
    im = msrc[f'640_conf_apd2 {{{channel_numbers[i]}}}']
    profile = im.sum(axis=(1,2))
    ax[0].plot(sted_power_axis[1:], profile[1:]/profile[1:].max(), label=f'{sted_pol_angles[i]}°')

ax[0].set_xlabel('Depletion power (W)')
ax[0].set_ylabel('Remaining intensity on APD2 (au)')
ax[0].set_title('Circular excitation')

channel_numbers = np.arange(11,16)
sted_pol_angles = np.arange(0, 181, 45)
sted_power_axis = 0.01 * np.linspace(.055, 1.25, 13)

for i in range(len(channel_numbers)):
    im = msrl[f'640_conf_apd2 {{{channel_numbers[i]}}}']
    profile = im.sum(axis=(1,2))
    ax[1].plot(sted_power_axis[1:], profile[1:]/profile.max(), label=sted_pol_angles[i])
ax[0 ].legend(title='Depletion\npolarisation')
ax[1].set_xlabel('Depletion power (W) \n TODO: correct for power nonlinearity')
# ax[1].set_ylabel('Remaining intensity (normalised)')
ax[1].set_title('Linear excitation')
ax[1].set_ylabel('Remaining intensity on APD2 (au)')

fig.savefig('../figures_generated/psted_beads.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_beads.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()