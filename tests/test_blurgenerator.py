import unittest
import numpy as np
from blurgenerator import motion_blur, lens_blur, gaussian_blur

class TestBlurGenerator(unittest.TestCase):

    def test_motion_blur(self):
        rgb = np.random.randint(255, size=(50, 50, 3),dtype=np.uint8)
        blur_img = motion_blur(rgb)
        self.assertFalse(np.array_equal(rgb, blur_img))

    def test_lens_blur(self):
        rgb = np.random.randint(255, size=(50, 50, 3),dtype=np.uint8)
        blur_img = lens_blur(rgb)
        self.assertFalse(np.array_equal(rgb, blur_img))

    def test_gaussian_blur(self):
        rgb = np.random.randint(255, size=(50, 50, 3),dtype=np.uint8)
        blur_img = gaussian_blur(rgb, kernel=3)
        self.assertFalse(np.array_equal(rgb, blur_img))

if __name__ == '__main__':
    unittest.main()
