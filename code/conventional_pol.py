# %%
import utils
import matplotlib.pyplot as plt

linewidth = (210-50)*.03937
figwidth = linewidth/2
figheight = 4.8 / 6.4 * figwidth
plt.rcParams['font.size'] = '6'

# %%
files = [
    r'../data/21-04-01 - 2b fov1 640 scan at 20%5x.msr',
    r'../data/21-04-01 - 2b fov2 640 scan at 20%5x.msr',
    r'../data/21-04-01 - 2b fov3 640 scan at 20%5x.msr',
]

msrs = [utils.read_msr(f) for f in files]
ims = [utils.align_stack(m['640_conf_apd2 {1}']) for m in msrs]

# %%
fig, ax = plt.subplots(1,len(files), figsize=(linewidth, figheight), dpi=300)

for i in range(len(files)):
    ax[i].imshow(utils.stack_to_rgb(ims[i]))
    ax[i].axis('off')
    utils.add_scalebar(ax[i], 10e-6/ims[i].pixel_size_xy)
    utils.add_colourwheel(ax[i])
    
fig.savefig('../figures_generated/conventional_pol.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/conventional_pol.svg', bbox_inches='tight')

# %%

fig, ax = plt.subplots(
    2,3, figsize=(linewidth, 2*figheight), 
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

    
fig.savefig('../figures_generated/conventional_pol_exps.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/conventional_pol_exps.svg', bbox_inches='tight')


# %%
utils.shutdown_jvm()