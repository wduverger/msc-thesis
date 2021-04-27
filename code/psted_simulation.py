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

def linear_mask(p1, p2, w=1):
    y1, x1 = p1
    y2, x2 = p2
        
    # Distance between points defining ROI
    dist0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    def dist(xy3):
        y0, x0 = xy3
        
        # Distance of point 0 to line
        dist = np.abs((x2-x1)*(y1-y0) - (x1-x0)*(y2-y1))/dist0
        
        # Length of vector x1 to x0 projected along line, as fraction of line length
        proj = ((x2-x1)*(x0-x1) + (y2-y1)*(y0-y1))/dist0**2
        
        # Calculate score only for points which are "next to" the ROI
        mask = np.where((0 <= proj) & (proj <= 1), 1/(dist+.001), 0)
        
        # Return a boolean mask. This threshold can be changed to account for width
        return mask > 1/w
    
    return dist

width=4
rod_0   = linear_mask(( 0,  N), (0, -N), w=width)((yy, xx))
rod_45  = linear_mask((-N, -N), (N,  N), w=width)((yy, xx))
rod_90  = linear_mask((-N,  0), (N,  0), w=width)((yy, xx))
rod_135 = linear_mask((-N,  N), (N, -N), w=width)((yy, xx))
rods = rod_0 | rod_45 | rod_90 | rod_135

proteins_cross = []
for i, j in zip(*np.where(xx | True)):
    if rods[i, j]:
        proteins_cross += [(1, i, j, np.arctan2(xx[i,j], yy[i,j]))]


# %% intensity calculations

def simulate(prot, psf, *args):
    result = np.zeros(xx.shape)
    for intensity, i, j, theta_p in prot:
        result[i, j] += intensity * psf(theta_p, *args)
    return result

def psf_circular(theta_p):
    return 1

def psf_linear(theta_p, theta_exc):
    return np.cos(theta_exc-theta_p)**2

def psf_psted(theta_p, theta_exc, psted=3):
    return np.cos(theta_exc-theta_p)**2 * np.exp(-psted * np.sin(theta_exc-theta_p)**2)

pol_angles = np.linspace(np.pi/2, -np.pi/2, 5)
img_circular = simulate(proteins, psf_circular)
imgs_linear = [simulate(proteins, psf_linear, theta_exc) for theta_exc in pol_angles]
imgs_psted  = [simulate(proteins, psf_psted,  theta_exc) for theta_exc in pol_angles]

rod_img_circular = simulate(proteins_cross, psf_circular)
rod_imgs_linear  = [simulate(proteins_cross, psf_linear, theta_exc) for theta_exc in pol_angles]
rod_imgs_psted   = [simulate(proteins_cross, psf_psted,  theta_exc) for theta_exc in pol_angles]


# %%
fig = plt.figure(figsize=(linewidth, 2*figheight), dpi=150)
gs = GridSpec(4, 6, figure=fig, hspace=0, width_ratios=[2.65, 1, 1, 1, 1,1])

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


ax = fig.add_subplot(gs[2:, 0])
ax.imshow(rod_img_circular)
ax.axis('off')
ax.set_title('Circular excitation', loc='left')
    
for i in range(5):
    ax = fig.add_subplot(gs[2, i+1])
    ax.imshow(rod_imgs_linear[i])
    ax.axis('off')

    if i==0:
        ax.set_title('Linear excitation', loc='left')

    ax = fig.add_subplot(gs[3, i+1])
    ax.imshow(rod_imgs_psted[i])
    ax.axis('off')

    if i==0:
        ax.set_title('pSTED', loc='left')

fig.savefig('../figures_generated/psted_simulation.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/psted_simulation.svg', bbox_inches='tight')
