import unittest
import os
import numpy as np
import math

import PIL.Image as Image

import sys

sys.path.append(".")

from src.utils import open_toml
from src.utils import save_image_buf
from src.utils import draw_bbox_on_image
from src.bbox import BoundingBox


def get_red_channel(i, j):
    return j


def get_blue_channel(i, j):
    return i


def get_green_channel(i, j):
    return i + j


def get_alpha_channel(i, j):
    return 0xFF


def draw_box(x, y, w, h, c):
    """Draws a box for grid cell s_ij

    The box has a center (x, y), width w and height h,
    and confidence c; displayed as line thickness.

    Args:
        x (float): x coordinate of center of box in grid cell [0, 1]
        y (float): y coordinate of center of box in grid cell [0, 1]
        w (float): width of box relative to input image [0, 1]
        h (float): height of box relative to input image [0, 1]
        c (float): probability that there exists an object in s_ij [0, 1]
    """
    pass


def get_pixel(i, j):
    """returns a pixel as an int

    Args:
        i (int): x coordinate of pixel
        j (int): y coordinate of pixel
    """
    r = get_red_channel(i, j)
    g = get_green_channel(i, j)
    b = get_blue_channel(i, j)
    a = get_alpha_channel(i, j)
    return get_rgba_int(r, g, b, a)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
        self.width = 375
        self.height = 500
        self.bbox1 = BoundingBox(
            self.width / 2, self.height / 2, self.width / 2, self.height / 2, 0.5
        )
        self.bbox2 = BoundingBox(
            self.width / 2 - self.width / 4 - self.width / 8,
            self.height / 2,
            self.width / 5,
            self.height / 6.5,
            0.5,
        )

    def test_open_toml(self):
        data = open_toml(self.path)
        self.assertIsInstance(data, dict)

    # def test_draw_bbox_on_buff(self):
    #     image_buf = np.zeros((self.width, self.height, 4), dtype=np.uint8)
    #     image_buf = draw_bbox_on_image(
    #         image_buf, [self.bbox1], size=(self.width, self.height)
    #     )
    #     image = Image.fromarray(image_buf, "RGBA")
    #     # image = image.rotate(90)
    #     image.save("test.png")

    def test_draw_bbox_on_image(self):
        with open(
            os.path.join(os.path.dirname(__file__), "../images/example.jpg"), "rb"
        ) as f:
            image_buf = np.array(Image.open(f))
            image_buf = draw_bbox_on_image(
                image_buf,
                [self.bbox1, self.bbox2],
            )
            image = Image.fromarray(image_buf, "RGB")
            image.save("../images/test.png")


if __name__ == "__main__":
    unittest.main()
