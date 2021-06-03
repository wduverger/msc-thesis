# %% 
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import hsv_to_rgb
import scipy.ndimage
import utils

# %%
def compensate_bleaching(stack):
    total_bleaching = stack[0].sum() / stack[-1].sum()
    bleaching_rate = np.power(total_bleaching, 1/len(stack))
    exp = np.power(bleaching_rate, np.arange(len(stack))).reshape(-1,1,1)
    return stack * exp

def gaussian_blur(stack, **kwargs):
    blurred = np.zeros_like(stack)
    
    for i in range(len(stack)):
        blurred[i] = scipy.ndimage.gaussian_filter(stack[i], **kwargs)
    return blurred

def sincomp(stack):
    pol_axis = np.arange(0, 171, 10)
    sin = np.sin(pol_axis * np.pi/90).reshape(-1,1,1)
    return (sin * stack).sum(axis=0)

def coscomp(stack):
    pol_axis = np.arange(0, 171, 10)
    cos = np.cos(pol_axis * np.pi/90).reshape(-1,1,1)
    return (cos * stack).sum(axis=0)

def pol_to_rgb(stack, blur=1, saturation=.2, brightness=.9):
    z,y,x = stack.shape
    image_hsv = np.zeros((y,x,3), dtype=np.float32)
    unbleached = compensate_bleaching(stack)
    blurred = gaussian_blur(unbleached, sigma=blur)
    
    sin = sincomp(blurred)
    cos = coscomp(blurred)
    h = np.arctan2(sin, cos) / (2 * np.pi) + .5
    s = np.sqrt(np.power(sin, 2) + np.power(cos, 2))
    v = unbleached.mean(axis=0)
    
    s = (s/s.max())**saturation
    v = (v/v.max())**brightness
    
    image_hsv[..., 0] = (h + 0.5) % 1
    image_hsv[..., 1] = s
    image_hsv[..., 2] = v
    return matplotlib.colors.hsv_to_rgb(image_hsv)


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

ring1 = build_target(    0,  N/5)
ring2 = build_target(4*N/5, N/10)

def simulate_target(psf, theta=0):
    theta_center = np.linspace(0, np.pi)
    intensity_center = psf(theta-theta_center).sum() / len(theta_center)
    return intensity_center * ring1 + psf(tt - theta) * ring2

theta_exc_target = np.linspace(0, 170/180*np.pi, 18)

colors_hsv = np.ones((len(theta_exc_target), 3))
colors_hsv[:, 0] = theta_exc_target / np.pi
colors_rgb = [hsv_to_rgb(colors_hsv[i]) for i in range(len(colors_hsv))]

def apply_color(image, color):
    image = image/image.max()
    image_rgb = np.zeros((*image.shape, 3))
    for i in range(3):
        image_rgb[..., i] = image * color[i]
    return image_rgb

image_stack = [simulate_target(psf_lin, t) for t in theta_exc_target]
image_rgb = pol_to_rgb(np.array(image_stack), saturation=1)

# %%

fig = plt.figure(figsize=(utils.linewidth, 0.8*utils.figheight), dpi=300)
w=1
gs = GridSpec(2, 10, figure=fig, hspace=-0.46)

# Plot circular excitation
ax = fig.add_subplot(gs[0:2, 0:2])
ax.imshow(simulate_target(psf_c), cmap='gray')
ax.axis('off')
# ax.set_title('Circular excitation', loc='left')

ax = fig.add_subplot(gs[0:2, -3:-1])
ax.imshow(image_rgb)
ax.axis('off')
# ax.set_title('False colour', loc='left')

for i in range(5):

    # Linear polarisation, gray
    ax = fig.add_subplot(gs[0, i+2])
    ax.imshow(image_stack[i*4], vmax=1, cmap='gray')
    ax.axis('off')

    # Target, psted
    ax = fig.add_subplot(gs[1, i+2])
    ax.imshow(apply_color(image_stack[i*4], colors_rgb[i*4]))
    ax.axis('off')

# %%


fig.savefig('../figures_generated/pol_simulation.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/pol_simulation.svg', bbox_inches='tight')