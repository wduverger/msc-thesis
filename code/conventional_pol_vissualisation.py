# # %%
# import utils
# import matplotlib.pyplot as plt
# from matplotlib.gridspec import GridSpec

# linewidth = (210-50)*.03937
# figwidth = linewidth/2
# figheight = 4.8 / 6.4 * figwidth
# plt.rcParams['font.size'] = '6'

# # %%
# file = r'../data/21-04-01 - 2b fov2 640 scan at 20%5x.msr'

# msr = utils.read_msr(file)
# img = utils.align_stack(msr['640_conf_apd2 {1}'])

# # %%

# shown_imgs = img[::3]
# n = len(shown_imgs)

# fig = plt.figure(dpi=200, figsize=(5,1))
# gs = GridSpec(2, n+1, figure=fig, width_ratios=([1]*n + [2]), hspace=.1, wspace=.1)

# def plotrow(imgs, row):
#     imgs2 = imgs**.5

#     for i in range(n):
#         ax = fig.add_subplot(gs[row, i])
#         ax.imshow(imgs2[i], vmax=imgs2.max(), vmin=0)
#         ax.axis('off')

#     ax = fig.add_subplot(gs[row, -1])
#     ax.plot(imgs.sum(axis=(1,2)))
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])

# plotrow(shown_imgs, 0)
# plotrow(utils.compensate_bleaching(shown_imgs), 1)


# # %%
# utils.shutdown_jvm()