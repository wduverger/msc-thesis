# %% definitions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

N = 200

x = np.arange(-N, N+1)
xx, yy = np.meshgrid(x, x)

rr = np.sqrt(xx**2 + yy**2)
grid_circle = (rr > 1000) & (rr < 1300)
grid_centre = rr < 70

# Construct protein population
proteins = []

for i, j in zip(*np.where(xx | True)):
    if rr[i, j] < N/5:
        proteins += [
            (1, i, j, theta) for theta in np.linspace(-np.pi, np.pi, 30)
        ]
    elif rr[i, j] > N * 4/5 - N/10 and rr[i, j] < N * 4/5 + N/10:
        proteins += [
            (30, i, j, np.arctan2(xx[i,j], yy[i,j]))
        ]

# %% intensity calculations

def simulate(psf, *args):
    result = np.zeros(xx.shape)
    for intensity, i, j, theta_p in proteins:
        result[i, j] += intensity * psf(theta_p, *args)
    return result

def psf_circular(theta_p):
    return 1

def psf_linear(theta_p, theta_exc):
    return np.cos(theta_exc-theta_p)**2

def psf_psted(theta_p, theta_exc, psted=3):
    return np.cos(theta_exc-theta_p)**2 * np.exp(-psted * np.sin(theta_exc-theta_p)**2)

pol_angles = np.linspace(0, 180, 5)
img_circular = simulate(psf_circular)
imgs_linear = [simulate(psf_linear, theta_exc) for theta_exc in pol_angles]
imgs_psted  = [simulate(psf_psted,  theta_exc) for theta_exc in pol_angles]


# %%
fig = plt.figure(figsize=(linewidth, figheight), dpi=150)
gs = GridSpec(2, 6, figure=fig, hspace=0, width_ratios=[2.65, 1, 1, 1, 1,1])

ax = fig.add_subplot(gs[0:2, 0])
ax.imshow(img_circular)
ax.axis('off')


ax.set_title('Circular excitation', loc='left')

for i in range(5):
    ax = fig.add_subplot(gs[0, i+1])
    ax.imshow(imgs_linear[i])
    ax.axis('off')

    if i==0:
        ax.set_title('Linear excitation', loc='left')

    ax = fig.add_subplot(gs[1, i+1])
    ax.imshow(imgs_psted[i])
    ax.axis('off')

    if i==0:
        ax.set_title('pSTED', loc='left')
    
fig.savefig('../figures_generated/psted_simulation.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_simulation.svg', bbox_inches='tight')
