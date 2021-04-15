#%%
import cv2
import matplotlib.colors
import numpy as np
import pandas as pd
import scipy.ndimage
import scipy.signal


def moving_average(array, n):
    return pd.Series(array).rolling(n).mean().values


def find_steps(y, average_window=200, **peaks_kwarg):
    """
    Fit a stepwise function to an array of function values 
    by locating peaks in the derivative
    """

    dy = np.abs(moving_average(np.diff(y), average_window))
    peaks, _ = scipy.signal.find_peaks(dy, **peaks_kwarg)

    left_bounds = np.hstack([0, peaks])
    right_bounds = np.hstack([peaks, -1])
    p_means = [
        y[l+average_window: r-average_window].mean()
        for l, r in zip(left_bounds, right_bounds)
    ]
    p_stds = [
        y[l+average_window: r-average_window].std()
        for l, r in zip(left_bounds, right_bounds)
    ]

    return left_bounds, np.array(p_means), np.array(p_stds)


def align_stack(original_image):
    """
    Align a stack of images (order of dimensions: zyx),
    only allowing translational motion
    """

    print('Opencv align...')

    corrected_image = np.zeros_like(original_image)
    corrected_image[0] = original_image[0]

    Z, Y, X = original_image.shape
    opencv_size = (X, Y)

    for i in range(Z - 1):
        reference = corrected_image[i]
        new_frame = original_image[i+1]

        num_iterations = int(1e6)
        eps = 1e-15
        criteria = (
            cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, num_iterations,
            eps
        )

        # Needs two implementations, depending on the opencv versian used
        warp_matrix = np.eye(2, 3, dtype=np.float32)
        try:
            (_, warp_matrix) = cv2.findTransformECC(
                reference, new_frame, warp_matrix,
                cv2.MOTION_TRANSLATION, criteria,
            )
        except TypeError:
            (_, warp_matrix) = cv2.findTransformECC(
                reference, new_frame, warp_matrix,
                cv2.MOTION_TRANSLATION, criteria,
                inputMask=None, gaussFiltSize=1
            )

        corrected_image[i+1] = cv2.warpAffine(
            new_frame, warp_matrix, opencv_size,
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        )

    return corrected_image


def compensate_bleaching(stack):
    i = np.arange(len(stack))
    total_bleaching = stack[-1].sum() / stack[0].sum()
    bleaching_rate = np.power(total_bleaching, 1/len(stack))
    exp = np.power(bleaching_rate, -i).reshape((-1, 1, 1))
    return stack * exp


def gaussian_blur(stack, **kwargs):
    blurred = np.zeros_like(stack)

    for i in range(len(stack)):
        blurred[i] = scipy.ndimage.gaussian_filter(stack[i], **kwargs)
    return blurred

def stack_to_rgb(stack, pol_axis=np.arange(0, 171, 10),
               blur_sigma=0, saturation=1, brightness=1):
    """
    Convert a stack of polarisation images into an RGB picture.
    """

    _, y, x = stack.shape
    image_hsv = np.zeros((y, x, 3), dtype=np.float32)

    unbleached = compensate_bleaching(stack)
    blurred = gaussian_blur(unbleached, sigma=blur_sigma)

    # Calculate Fourier coefficients
    sin = np.sin(pol_axis * np.pi/90).reshape((-1, 1, 1))
    cos = np.cos(pol_axis * np.pi/90).reshape((-1, 1, 1))
    sin = (sin * blurred).sum(axis=0)
    cos = (cos * blurred).sum(axis=0)

    # Define hue, saturation and value channels
    h = np.arctan2(sin, cos)
    v = unbleached.sum(axis=0)
    s = np.sqrt(np.power(sin, 2) + np.power(cos, 2)) / v

    # Ensure proper normalisation
    image_hsv[..., 0] = h / (2 * np.pi) + .5
    image_hsv[..., 1] = (s/s.max())**saturation
    image_hsv[..., 2] = (v/v.max())**brightness

    return matplotlib.colors.hsv_to_rgb(image_hsv)
