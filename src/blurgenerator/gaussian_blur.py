"""
Gaussian blur generator
"""

import cv2

def gaussian_blur(img, kernel, sigma=5):
    '''Gaussian blur generator'''
    if kernel % 2 == 0:
        kernel += 1
    kernel_size = (kernel, kernel)
    dst = cv2.GaussianBlur(img, kernel_size, sigma)
    return dst
