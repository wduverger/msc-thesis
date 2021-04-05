import numpy as np
import scipy.ndimage
import matplotlib.colors
import cv2


def align(original_image):
    corrected_image = np.zeros_like(original_image)
    corrected_image[0] = original_image[0]
    size = original_image[0].shape
    opencv_size = (size[1], size[0])
        
    for i in range(len(original_image) - 1):
        z = i + 1
        reference = corrected_image[z-1]
        new_frame = original_image[z]
        
        num_iterations = int(1e6)
        eps = 1e-15
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, num_iterations,  eps)

        
        warp_matrix = np.eye(2, 3, dtype=np.float32)
        (_, warp_matrix) = cv2.findTransformECC(reference, new_frame, warp_matrix,
                                                 cv2.MOTION_TRANSLATION, criteria)
        
        corrected_image[z] = cv2.warpAffine(new_frame, warp_matrix, opencv_size, 
                                            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    
    return corrected_image


def compensate_bleaching(stack):
    total_bleaching = stack[0].sum() / stack[-1].sum()
    bleaching_rate = np.power(total_bleaching, 1/len(stack))
    exp = np.power(bleaching_rate, np.arange(len(stack))).reshape((-1, 1, 1))
    return stack * exp


def gaussian_blur(stack, **kwargs):
    blurred = np.zeros_like(stack)

    for i in range(len(stack)):
        blurred[i] = scipy.ndimage.gaussian_filter(stack[i], **kwargs)
    return blurred


def pol_to_rgb(
    stack,
    pol_axis=np.arange(0, 171, 10),
    blur=1,
    saturation=.2,
    brightness=.9
):
    _, y, x = stack.shape
    image_hsv = np.zeros((y, x, 3), dtype=np.float32)

    unbleached = compensate_bleaching(stack)
    blurred = gaussian_blur(unbleached, sigma=blur)

    sin = np.sin(pol_axis * np.pi/90).reshape((-1, 1, 1))
    cos = np.cos(pol_axis * np.pi/90).reshape((-1, 1, 1))
    sin = (sin * blurred).sum(axis=0)
    cos = (cos * blurred).sum(axis=0)

    h = np.arctan2(sin, cos) / (2 * np.pi) + .5
    s = np.sqrt(np.power(sin, 2) + np.power(cos, 2))
    v = unbleached.sum(axis=0)

    image_hsv[..., 0] = h
    image_hsv[..., 1] = (s/s.max())**saturation
    image_hsv[..., 2] = (v/v.max())**brightness
    return matplotlib.colors.hsv_to_rgb(image_hsv)