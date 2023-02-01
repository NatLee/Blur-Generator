"""
Blur Maker
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

from blurgenerator import motion_blur, lens_blur, gaussian_blur
from blurgenerator.depth_mapping import blur_with_depth_layers

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

    args = parser.parse_args()

    if args.input:
        img_path = Path(args.input)
        if img_path.is_file():
            if img_path.suffix in ['.jpg', '.jpeg', '.png']:

                img = cv2.imread(img_path.absolute().as_posix())
                img = img / 255.

                if args.type not in ['motion', 'lens', 'gaussian']:
                    print('----- No type has been selected. Please specific `motion`, `lens`, or `gaussian`.')
                else:
                    if args.type == 'motion':
                        def blur_job(img, size=args.motion_blur_size):
                            return motion_blur(img, size=size, angle=args.motion_blur_angle)

                    elif args.type == 'lens':
                        def blur_job(img, radius=args.lens_radius):
                            return lens_blur(img, radius=radius, components=args.lens_components, exposure_gamma=args.lens_exposure_gamma)

                    elif args.type == 'gaussian':
                        def blur_job(img, kernel=args.gaussian_kernel):
                            return gaussian_blur(img, kernel)

                    if args.type in ['motion', 'lens', 'gaussian']:
                        depth_map_path = args.input_depth_map
                        if depth_map_path is None:
                            result = blur_job(img)
                        else:
                            result = np.zeros_like(img)
                            # need check path exists
                            depth_map = cv2.imread(depth_map_path)
                            mask_blur_amounts = blur_with_depth_layers(depth_map)
                            for mask, blur_amount in mask_blur_amounts:
                                slice = blur_job(img, blur_amount)
                                layer = cv2.bitwise_and(slice, slice, mask = mask[:,:,0])
                                result = cv2.add(result, layer, dtype=0)
                        cv2.imwrite(args.output, result)

            else:
                print('----- Only support common types of image `.jpg` and `.png`.')

        else:
            print('----- File not exists!')
    else:
        print('----- Please specific image for input.')
