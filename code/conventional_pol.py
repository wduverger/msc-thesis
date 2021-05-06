# %%
import utils
import matplotlib.pyplot as plt
import cv2

# %%
files = [
    r'../data/21-04-01 - 2b fov1 640 scan at 20%5x.msr',
    r'../data/21-04-01 - 2b fov2 640 scan at 20%5x.msr',
    r'../data/21-04-01 - 2b fov3 640 scan at 20%5x.msr',
]

msrs = [utils.read_msr(f) for f in files]
ims = [utils.align_stack(m['640_conf_apd2 {1}']) for m in msrs]

# %%

def scalebar_in_place(im, pad, height, width):
    width = int(width)
    im = im.copy()
    im[pad:pad+height, -pad-width:-pad, :] = [1, 1, 1]
    return im

def add_wheel(im, pad, resolution):
    wheel_im = utils.generate_wheel(resolution=resolution)
    Y, X, _ = wheel_im.shape
    wheel_rgb = wheel_im[..., 0:3]
    wheel_alpha = wheel_im[..., 3].astype(int).reshape(Y, X, 1)

    im = im.copy()
    im[pad:pad+Y, pad:pad+X] = wheel_alpha * wheel_rgb + (1-wheel_alpha) * im[pad:pad+Y, pad:pad+X]
    return im

for i in range(len(files)):
    im = utils.stack_to_rgb(ims[i])
    im = scalebar_in_place(im, pad=20, height=5, width=10e-6/ims[0].pixel_size_xy)
    im = add_wheel(im, pad=20, resolution=40)
    im *= 255
    
    cv2.imwrite(f'../figures_generated/conventional_pol_{i}.png', im)

# %%

fig, ax = plt.subplots(
    2,3, figsize=(utils.linewidth, 2*utils.figheight), 
    dpi=300, gridspec_kw=dict(hspace=0)
)

val_exp = [.1, .5, 1]
sat_exp = 1
for i in range(len(val_exp)):
    ax[0, i].imshow(utils.stack_to_rgb(ims[0], brightness=val_exp[i], saturation=sat_exp))
    ax[0, i].axis('off')
    utils.add_scalebar(ax[0, i], 10e-6/ims[i].pixel_size_xy)
    # utils.add_colourwheel(ax[0, i])
    ax[0, i].set(
        title=f'$\\alpha_v$ = {val_exp[i]} ($\\alpha_s$ = {sat_exp})'
    )

sat_exp = [.5, 1, 1.5]
val_exp = .5
for i in range(len(sat_exp)):
    ax[1, i].imshow(utils.stack_to_rgb(ims[0], 
        saturation=sat_exp[i], brightness=val_exp))
    ax[1, i].axis('off')
    utils.add_scalebar(ax[1, i], 10e-6/ims[i].pixel_size_xy)
    # utils.add_colourwheel(ax[1, i])
    ax[1, i].set(
        title=f'$\\alpha_s$ = {sat_exp[i]} ($\\alpha_v$ = {val_exp})'
    )

    
fig.savefig('../figures_generated/conventional_pol.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/conventional_pol.svg', bbox_inches='tight')


# %%
utils.shutdown_jvm()