
import numpy as np
import cv2

def map_range(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def blur_with_depth_layers(depth, num_layers=2, min_blur=1, max_blur=100):
    min_depth = np.min(np.unique(depth))
    max_depth = np.max(np.unique(depth))
    step = (max_depth - min_depth) // num_layers
    layers = np.array(range(min_depth, max_depth, step))
    mask_blur_amounts = []
    for value in layers:
        dm = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
        m = np.zeros(dm.shape)
        m[dm > value] = 255
        m[dm > (value + step)] = 0
        l_mask = depth.copy()
        l_mask[:,:,0] = m[:,:]
        l_mask[:,:,1] = m[:,:]
        l_mask[:,:,2] = m[:,:]
        _, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
        blur_amount = int(map_range(value, 0, 255, min_blur, max_blur))
        mask_blur_amounts.append((mask, blur_amount))
    return mask_blur_amounts
