import numpy as np
import cv2

from blurgenerator import motion_blur, lens_blur, gaussian_blur

def map_range(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def get_depth_step_and_layer(depth_map, num_layers):
    min_depth = np.min(np.unique(depth_map))
    max_depth = np.max(np.unique(depth_map))
    step = (max_depth - min_depth) // num_layers
    layers = np.array(range(min_depth, max_depth, step))
    return step, layers

def get_blur_amount_and_l_mask(depth_map, value, step, min_blur, max_blur):
    dm = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)
    m = np.zeros(dm.shape)
    m[dm > value] = 255
    m[dm > (value + step)] = 0
    l_mask = depth_map.copy()
    l_mask[:,:,0] = m[:,:]
    l_mask[:,:,1] = m[:,:]
    l_mask[:,:,2] = m[:,:]
    blur_amount = int(map_range(value, 0, 255, min_blur, max_blur))
    return blur_amount, l_mask

def blur_with_depth(depth_map, num_layers=10, min_blur=1, max_blur=100):
    step, layers = get_depth_step_and_layer(depth_map, num_layers)
    blur_masks = []
    for value in layers:
        blur_amount, l_mask = get_blur_amount_and_l_mask(
            depth_map,
            value,
            step,
            min_blur,
            max_blur
        )
        blur_masks.append((blur_amount, l_mask))
    return blur_masks

def motion_blur_with_depth_map(img, depth_map, angle=30, num_layers=10, min_blur=1, max_blur=100):
    out = np.zeros(img.shape)
    blur_masks = blur_with_depth(
        depth_map,
        num_layers=num_layers,
        min_blur=min_blur,
        max_blur=max_blur
    )
    for blur_amount, l_mask in blur_masks:
        slice = motion_blur(
            img,
            size=blur_amount,
            angle=angle
        )
        _, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
        layer = cv2.bitwise_and(slice, slice, mask=mask[:,:,0])
        out = cv2.add(out, layer, dtype=0)
    return out

def lens_blur_with_depth_map(img, depth_map, components=5, exposure_gamma=5, num_layers=10, min_blur=1, max_blur=100):
    out = np.zeros(img.shape)
    blur_masks = blur_with_depth(
        depth_map,
        num_layers=num_layers,
        min_blur=min_blur,
        max_blur=max_blur
    )

    for blur_amount, l_mask in blur_masks:
        slice = lens_blur(
            img,
            radius=blur_amount,
            components=components,
            exposure_gamma=exposure_gamma
        )
        _, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
        layer = cv2.bitwise_and(slice, slice, mask=mask[:,:,0])
        out = cv2.add(out, layer, dtype=0)
    return out

def gaussian_blur_with_depth_map(img, depth_map, sigma=5, num_layers=10, min_blur=1, max_blur=100):
    out = np.zeros(img.shape)
    blur_masks = blur_with_depth(
        depth_map,
        num_layers=num_layers,
        min_blur=min_blur,
        max_blur=max_blur
    )

    for blur_amount, l_mask in blur_masks:
        slice = gaussian_blur(
            img,
            blur_amount,
            sigma=sigma
        )
        _, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
        layer = cv2.bitwise_and(slice, slice, mask=mask[:,:,0])
        out = cv2.add(out, layer, dtype=0)
    return out