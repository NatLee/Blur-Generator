"""
Blur maker init
"""
__version__ = "1.0.0"

from .motion_blur import motion_blur
from .lens_blur import lens_blur
from .gaussian_blur import gaussian_blur

from .cli import main
