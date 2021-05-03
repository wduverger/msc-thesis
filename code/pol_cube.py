# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import utils

data = pd.read_csv(
    '../data/21-03-09 - pol cube on test bench.csv', sep=';', 
    header=1, decimal=',', skipfooter=4, engine='python'
)

fig, ax = plt.subplots(figsize=(utils.figwidth, utils.figheight))

ax.plot(data['pol angle'], data['pT/max'], '.-', label='Transmitted')
ax.plot(data['pol angle'], data['pR/max'], '.-', label='Reflected')
ax.set(
    xlabel='Incoming polarisation (deg)',
    xticks=np.arange(0,181, 30),
    ylabel='Power (normalised)',
)
ax.legend()

print(f'min(pR) = {data["pR/max"].min()}')
print(f'min(pT) = {data["pT/max"].min()}')

fig.savefig('../figures_generated/pol_cube.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/pol_cube.svg', bbox_inches='tight')
