"""
Motion blur generator

"""

from random import randint

import cv2
import numpy as np

def motion_blur(img, size=None, angle=None):
    '''Motion blur generator'''
    if size is None:
        size = randint(20, 80)
    if angle is None:
        angle = randint(15, 30)

    k = np.zeros((size, size), dtype=np.float32)
    k[(size-1)//2, :] = np.ones(size, dtype=np.float32)
    k = cv2.warpAffine(k, cv2.getRotationMatrix2D((size/2-0.5, size/2-0.5), angle, 1.0), (size, size))
    k = k * (1.0/np.sum(k))

    return cv2.filter2D(img, -1, k)
