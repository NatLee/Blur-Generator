
# Blur Generator

Generate blur on image.

There are 3 types of blur can be used with `motion`, `lens`, or `gaussian`.

We can use the results on model training or something.

## Usage

```bash
usage: main.py [-h] [--input INPUT] [--output OUTPUT] [--type TYPE] [--motion_blur_size MOTION_BLUR_SIZE]
               [--motion_blur_angle MOTION_BLUR_ANGLE] [--lens_radius LENS_RADIUS] [--lens_components LENS_COMPONENTS]
               [--lens_exposure_gamma LENS_EXPOSURE_GAMMA] [--gaussian_kernel GAUSSIAN_KERNEL]

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

## Results

* Original image

![original image](./doc/test.png)

* Motion blur

`python3 main.py --type motion --input ./doc/test.png --output ./doc/motion.png`

![motion blur image](./doc/motion.png)

* Lens blur

`python3 main.py --type lens --input ./doc/test.png  --output ./doc/lens.png`

![lens blur image](./doc/lens.png)

* Gaussian blur

`python3 main.py --type gaussian --input ./doc/test.png --output ./doc/gaussian.png`

![gaussian blur image](./doc/gaussian.png)

