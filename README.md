# Blur Generator

This tool is for generating blur on images.

There are 3 types of blur modes of `motion`, `lens`, or `gaussian`.

We can use the results on model training or something else.

## Installation

```bash
pip install blurgenerator
```

## Usage

```bash
usage: blurgenerator [-h] [--input INPUT] [--output OUTPUT] [--type TYPE] [--motion_blur_size MOTION_BLUR_SIZE] [--motion_blur_angle MOTION_BLUR_ANGLE]
                     [--lens_radius LENS_RADIUS] [--lens_components LENS_COMPONENTS] [--lens_exposure_gamma LENS_EXPOSURE_GAMMA]
                     [--gaussian_kernel GAUSSIAN_KERNEL]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Specific path of image as `input`.
  --output OUTPUT       Specific path for `output`. Default is `./result.png`.
  --type TYPE           Blur type of `motion`, `lens`, or `gaussian`. Default is `motion`.
  --motion_blur_size MOTION_BLUR_SIZE
                        Size for motion blur. Default is 100.
  --motion_blur_angle MOTION_BLUR_ANGLE
                        Angle for motion blur. Default is 30.
  --lens_radius LENS_RADIUS
                        Radius for lens blur. Default is 5.
  --lens_components LENS_COMPONENTS
                        Components for lens blur. Default is 4.
  --lens_exposure_gamma LENS_EXPOSURE_GAMMA
                        Exposure gamma for lens blur. Default is 2.
  --gaussian_kernel GAUSSIAN_KERNEL
                        Kernel for gaussian. Default is 100.
```

## Example and Result

- Original image

![original image](./doc/test.png)

- Motion blur

`blurgenerator --type motion --input ./doc/test.png --output ./doc/motion.png`

```python
import cv2
from blurgenerator import motion_blur
img = cv2.imread('test.png')
result = motion_blur(img, size=100, angle=30)
```

![motion blur image](./doc/motion.png)

- Lens blur

`blurgenerator--type lens --input ./doc/test.png --output ./doc/lens.png`

```python
import cv2
from blurgenerator import lens_blur
img = cv2.imread('test.png')
result = lens_blur(img, radius=5, components=4, exposure_gamma=2)
```

![lens blur image](./doc/lens.png)

- Gaussian blur

`blurgenerator --type gaussian --input ./doc/test.png --output ./doc/gaussian.png`

```python
import cv2
from blurgenerator import gaussian_blur
img = cv2.imread('test.png')
result = gaussian_blur(img, 100)
```

![gaussian blur image](./doc/gaussian.png)
