# %%

import numpy as np
import matplotlib.pyplot as plt
import utils

def plot_empty(ax):
    ax.set_aspect(1)
    ax.set(xlim=[-1,1], ylim=[-1,1], xticks=[], yticks=[])
    ax.axis('off')      
    ax.axhline(0, color='k', linewidth=.3)
    # ax.axvline(0, color='k', linewidth=.3)
    # removing the default axis on all sides:
    # for side in ['bottom','right','top','left']:
    #     ax.spines[side].set_visible(False)  

def plot_pol_ellipse(ax, jvec):
    ex = jvec[0,0]
    ey = jvec[1,0]

    t = np.linspace(0, 2*np.pi)
    x = np.real(ex * np.exp(1j * t))
    y = np.real(ey * np.exp(1j * t))
    d = np.angle(ey/ex)

    lefthanded = d > 0
    circular = d % np.pi > .5 and np.abs(ex) > .2 and np.abs(ey) > .2
    color = 'C0' if not circular else (
        'C1' if lefthanded else 'C2'
    )
    ax.plot(x, y, color=color)

n = 9

# Construct initial Jones vectors: list of linear ones, Rcircular and Lcircular
jvec = [
    np.array([[np.cos(t)], [np.sin(t)]]) 
    for t in np.linspace(0, np.pi, n)
] + [
    1/np.sqrt(2) * np.array([[1], [1j]]),
    1/np.sqrt(2) * np.array([[1], [-1j]])
]

# Jones matrices
s2 = np.array([[1, 0], [0, -1]])
s4 = np.array([[1, 0], [0, 1j]])

# Visualise action of waveplates
fig, ax = plt.subplots(3, len(jvec), 
    figsize=(utils.linewidth, utils.figheight),
    gridspec_kw=dict(hspace=1))

for i, j in enumerate(jvec):
    plot_empty(ax[0, i])
    plot_empty(ax[1, i])
    plot_empty(ax[2, i])

    plot_pol_ellipse(ax[0, i],           j)
    plot_pol_ellipse(ax[1, i],      s2 @ j)
    plot_pol_ellipse(ax[2, i], s4 @ s2 @ j)

ax[0, 0].set_title('1. Initial', loc='left')
ax[1, 0].set_title('2. After QWP', loc='left')
ax[2, 0].set_title('3. After QWP and HWP', loc='left')

fig.savefig('../figures_generated/waveplates.pdf')#, bbox_inches='tight')
fig.savefig('../figures_generated/waveplates.svg')#, bbox_inches='tight')
