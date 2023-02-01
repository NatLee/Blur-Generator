# Blur Generator

[![Test](https://github.com/NatLee/Blur-Generator/actions/workflows/test.yml/badge.svg)](https://github.com/NatLee/Blur-Generator/actions/workflows/test.yml)[![Release](https://github.com/NatLee/Blur-Generator/actions/workflows/release.yml/badge.svg)](https://github.com/NatLee/Blur-Generator/actions/workflows/release.yml)

This tool is for generating blur on images.

There are 3 types of blur modes of `motion`, `lens`, or `gaussian`.

We can use the results on model training or something else.

## Installation

```bash
pip install blurgenerator
```

Check it on [Pypi](https://pypi.org/project/BlurGenerator/).

## Usage

```bash
blurgenerator --help
```

```bash
usage: blurgenerator [-h] [--input INPUT] [--input_depth_map INPUT_DEPTH_MAP] [--output OUTPUT] [--type TYPE] [--motion_blur_size MOTION_BLUR_SIZE] [--motion_blur_angle MOTION_BLUR_ANGLE] [--lens_radius LENS_RADIUS] [--lens_components LENS_COMPONENTS]
                     [--lens_exposure_gamma LENS_EXPOSURE_GAMMA] [--gaussian_kernel GAUSSIAN_KERNEL] [--depth_num_layers DEPTH_NUM_LAYERS] [--depth_min_blur DEPTH_MIN_BLUR] [--depth_max_blur DEPTH_MAX_BLUR]
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
  --depth_num_layers DEPTH_NUM_LAYERS
                        Layer for depth blur. Default is 3.
  --depth_min_blur DEPTH_MIN_BLUR
                        Min. blur for depth blur. Default is 1.
  --depth_max_blur DEPTH_MAX_BLUR
                        Max. blur for depth blur. Default is 100.
```

## Example and Result

### Common use

- Original image

![original image](./doc/test.png)

#### Usage

- Motion blur

`blurgenerator --type motion --input ./doc/test.png --output ./doc/motion.png`

```python
import cv2
from blurgenerator import motion_blur
img = cv2.imread('test.png')
result = motion_blur(img, size=100, angle=30)
cv2.imwrite('./output.png', result)
```

![motion blur image](./doc/motion.png)

- Lens blur

`blurgenerator--type lens --input ./doc/test.png --output ./doc/lens.png`

```python
import cv2
from blurgenerator import lens_blur
img = cv2.imread('test.png')
result = lens_blur(img, radius=5, components=4, exposure_gamma=2)
cv2.imwrite('./output.png', result)
```

![lens blur image](./doc/lens.png)

- Gaussian blur

`blurgenerator --type gaussian --input ./doc/test.png --output ./doc/gaussian.png`

```python
import cv2
from blurgenerator import gaussian_blur
img = cv2.imread('test.png')
result = gaussian_blur(img, 100)
cv2.imwrite('./output.png', result)
```

![gaussian blur image](./doc/gaussian.png)

### With depth map

Feature from this [issue](https://github.com/NatLee/Blur-Generator/issues/1).

- Original image

![photo](./doc/depth-test.jpg)

- Depth map

![depth map](./doc/depth-map-test.png)

#### Usage

- Motion blur with depth map

`blurgenerator --input .\doc\depth-test.jpg --type motion --input_depth_map .\doc\depth-map-test.png --depth_num_layers 5 --depth_min_blur 1 --depth_max_blur 50 --output .\doc\depth-motion-output.png`

```python
import cv2
from blurgenerator import motion_blur_with_depth_map
img = cv2.imread('test.jpg')
depth_img = cv2.imread('test-depth.png')
result = motion_blur_with_depth_map(
   img,
   depth_map=depth_img,
   angle=30,
   num_layers=10,
   min_blur=1,
   max_blur=50
)
cv2.imwrite('./output.png', result)
```

![depth motion blur image](./doc/depth-motion-output.png)

- Lens blur with depth map

`blurgenerator --input .\doc\depth-test.jpg --type lens --input_depth_map .\doc\depth-map-test.png --depth_num_layers 3 --depth_min_blur 1 --depth_max_blur 50 --output .\doc\depth-lens-output.png`

```python
import cv2
from blurgenerator import lens_blur_with_depth_map
img = cv2.imread('test.jpg')
depth_img = cv2.imread('test-depth.png')
result = lens_blur_with_depth_map(
   img,
   depth_map=depth_img,
   components=5,
   exposure_gamma=5,
   num_layers=10,
   min_blur=1,
   max_blur=50
)
cv2.imwrite('./output.png', result)
```

![depth lens blur image](./doc/depth-lens-output.png)

- Gaussian blur with depth map

`blurgenerator --input .\doc\depth-test.jpg --type gaussian --input_depth_map .\doc\depth-map-test.png --depth_num_layers 3 --depth_min_blur 1 --depth_max_blur 50 --output .\doc\depth-gaussian-output.png`

```python
import cv2
from blurgenerator import gaussian_blur_with_depth_map
img = cv2.imread('test.jpg')
depth_img = cv2.imread('test-depth.png')
result = gaussian_blur_with_depth_map(
   img,
   depth_map=depth_img,
   sigma=5,
   num_layers=10,
   min_blur=1,
   max_blur=50
)
cv2.imwrite('./output.png', result)
```

![depth gaussian blur image](./doc/depth-gaussian-output.png)
