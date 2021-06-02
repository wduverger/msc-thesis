# %%

import numpy as np
import utils
import matplotlib.pyplot as plt

# %%

file = r'../data/21-05-26 - photobleaching_2.msr'
msr = utils.read_msr(file)
utils.shutdown_jvm()

# %%

stack = msr['640_conf_apd2 {1}']

fig, ax = plt.subplots(1,2, gridspec_kw=dict(
    # width_ratios=[4,1],
    wspace=.5
))
ax[0].imshow(stack[0])
ax[0].axis('off')

profile = stack.sum(axis=(1,2))
# tt = np.arange(len(profile))
# bleach = np.power(profile[-1]/profile[0], tt/len(profile))
ax[1].plot(profile/profile.max())
# ax[1].plot(bleach)
ax[1].set(
    xlabel='Frame number',
    ylabel='Intensity (norm)',
    xticks=np.arange(0, len(profile)+1, 5)
)

fig.savefig('../figures_generated/photobleaching.svg', bbox_inches='tight')
fig.savefig('../figures_generated/photobleaching.pdf', bbox_inches='tight')