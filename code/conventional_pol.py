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
ims = [utils.align(m['640_conf_apd2 {1}']) for m in msrs]
# %%
fig, ax = plt.subplots(1,len(files), figsize=(linewidth, figheight), dpi=300)

for i in range(len(files)):
    ax[i].imshow(utils.pol_to_rgb(ims[i], blur=0, brightness=.7, saturation=.6))
    ax[i].axis('off')
    utils.add_scalebar(ax[i], 10e-6/ims[i].pixel_size_xy)

fig.savefig('../figures/conventional_pol.pdf')
fig.savefig('../figures/conventional_pol.svg')

# %%
utils.shutdown_jvm()