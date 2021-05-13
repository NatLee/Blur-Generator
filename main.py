"""
Blur Maker

"""
import argparse

from pathlib import Path

import cv2

from blur_tools import motion_blur, lens_blur, gaussian_blur


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default=None, help='Specific path of image as `input`.')
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
                    print('No type has been selected. Please specific `motion`, `lens`, or `gaussian`.')
                else:
                    if args.type == 'motion':
                        result = motion_blur(img, size=args.motion_blur_size, angle=args.motion_blur_angle)

                    elif args.type == 'lens':
                        result = lens_blur(img, radius=5, components=4, exposure_gamma=2)

                    elif args.type == 'gaussian':
                        result = gaussian_blur(img, 100)

                    cv2.imwrite(args.output, result*255)

            else:
                print('Only support common types of image `.jpg` and `.png`.')

        else:
            print('File not exists!')
    else:
        print('Please specific image for input.')
