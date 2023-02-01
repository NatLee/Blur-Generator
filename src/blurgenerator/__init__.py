"""
Blur maker init
"""
__version__ = "1.0.2"

from .motion_blur import motion_blur
from .lens_blur import lens_blur
from .gaussian_blur import gaussian_blur

from .depth_mapping import blur_with_depth_layers

from .cli import main
