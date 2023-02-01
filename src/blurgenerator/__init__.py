"""
Blur maker init
"""
__version__ = "1.0.2"

from .motion_blur import motion_blur
from .lens_blur import lens_blur
from .gaussian_blur import gaussian_blur

from .depth import motion_blur_with_depth_map
from .depth import lens_blur_with_depth_map
from .depth import gaussian_blur_with_depth_map

from .cli import main
