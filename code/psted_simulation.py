# %% 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import utils

# %%

N = 200
x = np.arange(-N, N+1)
xx, yy = np.meshgrid(x, x)
rr = np.sqrt(xx**2 + yy**2)
tt = np.arctan2(yy, xx)

psf_c     = lambda dtheta: np.ones_like(dtheta)
psf_lin   = lambda dtheta: np.cos(dtheta)**2
psf_psted = lambda dtheta: np.cos(dtheta)**2 * np.exp(-100*np.sin(dtheta)**2)

def build_target(ring_center, ring_width):
    return np.abs(rr - ring_center) < ring_width

def simulate_target(psf, theta=0):
    theta_center = np.linspace(0, np.pi)
    intensity_center = psf(theta-theta_center).sum() / len(theta_center)
    return intensity_center * ring1 + psf(tt - theta) * ring2

def build_grid(angle, pitch, width):
    y0 = xx * np.tan(angle)
    dy = yy - y0
    return (dy % pitch) < width

angle = 10 * np.pi/180
pitch = 30
width = 10
grid1 = build_grid( angle, pitch, width)
grid2 = build_grid(-angle, pitch, width)

ring1 = build_target(    0,  N/5)
ring2 = build_target(4*N/5, N/10)

def simulate_grid(psf, theta=0):
    return psf(angle - theta) * grid1 + psf(-angle - theta) * grid2

theta_exc_target = np.linspace(0, np.pi, 5)
theta_exc_grid = np.linspace(-2*angle, 2*angle, 5)

fig = plt.figure(figsize=(utils.linewidth, 2*utils.figheight), dpi=150)
gs = GridSpec(4, 6, figure=fig, hspace=0, width_ratios=[2.65, 1, 1, 1, 1,1])

# Plot circular excitations
ax = fig.add_subplot(gs[0:2, 0])
ax.imshow(simulate_target(psf_c))
ax.axis('off')
ax.set_title('Circular excitation', loc='left')

ax = fig.add_subplot(gs[2:, 0])
ax.imshow(simulate_grid(psf_c))
ax.axis('off')
ax.set_title('Circular excitation', loc='left')

for i in range(5):

    # Target, linear
    ax = fig.add_subplot(gs[0, i+1])
    ax.imshow(simulate_target(psf_lin, theta_exc_target[i]), vmax=1)
    ax.axis('off')
    # ax.set_title(np.rad2deg(theta_exc_target[i]).astype(int), loc='right')
    if i==0:
        ax.set_title('no pSTED', loc='left')

    # Target, psted
    ax = fig.add_subplot(gs[1, i+1])
    ax.imshow(simulate_target(psf_psted, theta_exc_target[i]), vmax=1)
    ax.axis('off')
    # ax.set_title(np.rad2deg(theta_exc_target[i]).astype(int), loc='right')
    if i==0:
        ax.set_title('pSTED', loc='left')

    # Grid, linear
    ax = fig.add_subplot(gs[2, i+1])
    ax.imshow(simulate_grid(psf_lin, theta_exc_grid[i]), vmax=1)
    ax.axis('off')
    # ax.set_title(np.rad2deg(theta_exc_grid[i]).astype(int), loc='right')
    if i==0:
        ax.set_title('no pSTED', loc='left')

    # Grid, psted
    ax = fig.add_subplot(gs[3, i+1])
    ax.imshow(simulate_grid(psf_psted, theta_exc_grid[i]), vmax=1)
    ax.axis('off')
    # ax.set_title(np.rad2deg(theta_exc_grid[i]).astype(int), loc='right')
    if i==0:
        ax.set_title('pSTED', loc='left')

# %%


fig.savefig('../figures_generated/psted_simulation.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_simulation.svg', bbox_inches='tight')

# %%

fig, ax = plt.subplots(1, 1, figsize=(0.5*utils.linewidth, utils.figheight))

t = np.linspace(-90, 90, 500)
tr = t * np.pi / 180
ax.plot(t, (psf_lin(tr-angle) + psf_lin(tr+angle))/2, label='no pSTED')
ax.plot(t, psf_psted(tr-angle) + psf_psted(tr+angle), label='pSTED')
ax.set(
    xlabel='Excitation polarisation (deg)',
    ylabel='Intensity (norm)',
    xticks=np.arange(-90, 91, 45)
)
ax.legend(loc='upper right')

fig.savefig('../figures_generated/psted_simulation_profile.svg', bbox_inches='tight')