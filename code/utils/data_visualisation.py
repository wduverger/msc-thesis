import numpy as np

import matplotlib.colors
import mpl_toolkits.axes_grid1.anchored_artists as mpl_aa
import mpl_toolkits.axes_grid1.inset_locator as mpl_il


def add_scalebar(axis, len_in_pixels, label=None, position='upper right',
                 color='white', frameon=False, pad=.3, size_vertical=2, **kwargs):
    """ Add scalebar to a plot with sensible defaults """

    axis.add_artist(mpl_aa.AnchoredSizeBar(
        axis.transData, len_in_pixels, label, position, color=color,
        frameon=frameon, size_vertical=size_vertical, pad=pad,
        **kwargs
    ))


def add_colourwheel(axis, loc='upper left', size=.12, **wheel_kw):
    """ 
    Add a colourwheel to a plot. 
    Use `wheel_kw` to choose alpha, saturation, etc of the wheel image
    """

    wheel_im = generate_wheel(**wheel_kw)

    inset = mpl_il.inset_axes(
        axis, loc='upper left', width=size, height=size
    )
    inset.axis('off')
    inset.imshow(wheel_im)


def generate_wheel(alpha=1, sat=1, val=.9, resolution=100):
    x = np.linspace(-1, 1, resolution)
    y = np.linspace(-1, 1, resolution)

    xx, yy = np.meshgrid(x, y)
    im_hsv = np.zeros((*xx.shape, 3))

    rr = np.sqrt(xx**2 + yy**2)  # Distance from origin
    tt = np.arctan2(yy, -xx)     # Angle of pixel vector to x axis

    disc = rr < 1  # Image that is 0 if pixel outside unit circle, 1 otherwise

    im_hsv[..., 0] = disc*tt / (2*np.pi) + 0.5  # Hue
    im_hsv[..., 1] = disc*rr * sat              # Saturation
    im_hsv[..., 2] = disc * val                 # Brightness

    # Convert to RGB
    im_hsv = matplotlib.colors.hsv_to_rgb(im_hsv)
    im_rgb = np.zeros((*xx.shape, 4))
    im_rgb[..., 0:3] = im_hsv

    # Add alpha channel 
    # alpha should be 0 outside the disk, otherwise the image will be black
    im_rgb[..., 3] = disc * alpha

    return im_rgb
