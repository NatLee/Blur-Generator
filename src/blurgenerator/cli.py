"""
Blur Maker
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

from blurgenerator import motion_blur, lens_blur, gaussian_blur

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Specific path of image as `input`.')
    parser.add_argument('--input_depth_map', type=str, default=None, help='Specific path of depth image as `input_depth_map`.')

    parser.add_argument('--output', type=str, default='./result.png', help='Specific path for `output`. Default is `./result.png`.')

    parser.add_argument('--type', type=str, default='motion', help='Blur type of `motion`, `lens`, or `gaussian`. Default is `motion`.')

    parser.add_argument('--motion_blur_size', type=int, default=100, help='Size for motion blur. Default is 100.')
    parser.add_argument('--motion_blur_angle', type=int, default=30, help='Angle for motion blur. Default is 30.')

    parser.add_argument('--lens_radius', type=int, default=5, help='Radius for lens blur. Default is 5.')
    parser.add_argument('--lens_components', type=int, default=4, help='Components for lens blur. Default is 4.')
    parser.add_argument('--lens_exposure_gamma', type=int, default=2, help='Exposure gamma for lens blur. Default is 2.')

    parser.add_argument('--gaussian_kernel', type=int, default=100, help='Kernel for gaussian. Default is 100.')

    # depth blur settings
    parser.add_argument('--depth_num_layers', type=int, default=10, help='Layer for depth blur. Default is 3.')
    parser.add_argument('--depth_min_blur', type=int, default=1, help='Min. blur for depth blur. Default is 1.')
    parser.add_argument('--depth_max_blur', type=int, default=100, help='Max. blur for depth blur. Default is 100.')

    # ---------------------------------------------------------------

    args = parser.parse_args()

    if not args.input:
        print('----- Please specific image for input.')
        return

    img_path = Path(args.input)

    if not img_path.is_file():
        print('----- `img_path` is not a file!')
        return

    if img_path.suffix not in ['.jpg', '.jpeg', '.png']:
        print('----- Only support common types of image `.jpg` and `.png`.')
        return

    if args.type not in ['motion', 'lens', 'gaussian']:
        print('----- No type has been selected. Please specific `motion`, `lens`, or `gaussian`.')
        return

    if args.type == 'motion':
        def blur_job(img, size=args.motion_blur_size):
            return motion_blur(img, size=size, angle=args.motion_blur_angle)

    if args.type == 'lens':
        def blur_job(img, radius=args.lens_radius):
            return lens_blur(img, radius=radius, components=args.lens_components, exposure_gamma=args.lens_exposure_gamma)

    if args.type == 'gaussian':
        def blur_job(img, kernel=args.gaussian_kernel):
            return gaussian_blur(img, kernel)

    # ---------------------------------------------------------------

    img = cv2.imread(img_path.absolute().as_posix())

    depth_map_path = args.input_depth_map

    if depth_map_path is None:
        print(f'----- Generating `{args.type}` blur.')
        result = blur_job(img)
        cv2.imwrite(args.output, result)
        return

    depth_map_path = Path(depth_map_path)
    if not depth_map_path.is_file():
        print('----- `input_depth_map` is not a file!')
        return
    if depth_map_path.suffix not in ['.jpg', '.jpeg', '.png']:
        print('----- Only support common types of image `.jpg` and `.png`.')
        return

    print(f'----- Generating `{args.type}` blur with depth map.')
    print('----- `motion_blur_size` will be ignored.')
    print('----- `lens_radius` will be ignored.')
    print('----- `gaussian_kernel` will be ignored.')

    depth_map = cv2.imread(depth_map_path.absolute().as_posix())

    def map_range(value, inMin, inMax, outMin, outMax):
        return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

    def blur_with_depth(img, depth, num_layers=10, min_blur=1, max_blur=100):
        min_depth = np.min(np.unique(depth))
        max_depth = np.max(np.unique(depth))
        step = (max_depth - min_depth) // num_layers
        layers = np.array(range(min_depth, max_depth, step))
        out = np.zeros(img.shape)

        for value in layers:
            dm = cv2.cvtColor(depth, cv2.COLOR_BGR2GRAY)
            m = np.zeros(dm.shape)
            m[dm > value] = 255
            m[dm > (value + step)] = 0
            l_mask = depth.copy()
            l_mask[:,:,0] = m[:,:]
            l_mask[:,:,1] = m[:,:]
            l_mask[:,:,2] = m[:,:]
            blur_amount = int(map_range(value, 0, 255, min_blur, max_blur))
            slice = blur_job(img, blur_amount)
            _, mask = cv2.threshold(l_mask, 100, 255, cv2.THRESH_BINARY)
            layer = cv2.bitwise_and(slice, slice, mask = mask[:,:,0])
            out = cv2.add(out, layer, dtype=0)
        return out

    num_layers = args.depth_num_layers
    min_blur = args.depth_min_blur
    max_blur = args.depth_max_blur

    result = blur_with_depth(img, depth_map, num_layers=num_layers, min_blur=min_blur, max_blur=max_blur)
    cv2.imwrite(args.output, result)

    return

