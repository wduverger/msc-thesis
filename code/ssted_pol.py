# %%
 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import scipy.optimize

import utils

filename = '../data/20-12-01 - 02_conf-640-12_conf-561-5_sted-640-17-10_sted-561-10-10_083au_linac-10_scan-640-0-175-5.msr'
msr = utils.read_msr(filename)

# %%

im_act_stack = msr['640_sted_apd2 {8}']

roi_1 = [(348,  525), 120, 120]
roi_2 = [(430, 1210), 120, 120]

fig = plt.figure(figsize=(utils.linewidth, utils.figheight))
gs = plt.GridSpec(2, 2, figure=fig, hspace=.5, wspace=.4)

# Plot image
show_img = im_act_stack[0]/im_act_stack[0].max() * 2
show_img[show_img > 1] = 1

ax = fig.add_subplot(gs[:, 0])
ax.imshow(show_img, cmap='gray')
ax.add_patch(Rectangle(
    *roi_1, fill=False, lw=1, color='C1'
))
ax.add_patch(Rectangle(
    *roi_2, fill=False, lw=1, color='C2'
))
utils.add_scalebar(ax, 10e-6/show_img.pixel_size_xy, '10 μm')
ax.axis('off')

# Plot profiles
ax1 = fig.add_subplot(gs[0, 1])
ax0 = fig.add_subplot(gs[1, 1])
norm = lambda x: (x-x.min())/(x.max()-x.min())
exp = lambda x, rate: np.exp(x * rate)

# - calculate bleaching curve
x_axis = (np.linspace(0,175, 5) / 5).round() * 5
opt_rate, conf = scipy.optimize.curve_fit(exp, x_axis, norm(im_act_stack.sum(axis=(1,2))))
ax1.plot(x_axis, np.exp(x_axis * opt_rate), 'k:', alpha=.3)
ax0.hlines(0, 0, 175, ls=':', alpha=.3)

# - calculate profiles
((x0, y0), dx, dy) = roi_1
p1 = norm(im_act_stack[:, y0:y0+dy, x0:x0+dx].sum(axis=(1,2)))
((x0, y0), dx, dy) = roi_2
p2 = norm(im_act_stack[:, y0:y0+dy, x0:x0+dx].sum(axis=(1,2)))

# - plot profiles
ax1.plot(x_axis, p1, '.-', color='C1')
ax1.plot(x_axis, p2, '.-', color='C2')
ax0.plot(x_axis, p1-np.exp(x_axis * opt_rate), '.-', color='C1')
ax0.plot(x_axis, p2-np.exp(x_axis * opt_rate), '.-', color='C2')

# - figure markup
ax0.set(
    title='Bleaching subtracted',
    ylabel='Intensity',
    xlabel='Excitation polarisation (deg)',
    xticks=x_axis
)
ax1.set(
    title='Original',
    ylabel='Intensity',
    xticks=x_axis,
    xticklabels=[],
)

fig.savefig('../figures_generated/ssted_pol.pdf', bbox_inches='tight')
fig.savefig('../figures_generated/ssted_pol.svg', bbox_inches='tight')

# %%
utils.shutdown_jvm()


