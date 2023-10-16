import unittest
import os
import numpy as np
import math

import PIL.Image as Image

from src.utils import open_toml
from src.utils import save_image_buf


def get_red_channel(i, j):
    return j


def get_blue_channel(i, j):
    return i


def get_green_channel(i, j):
    return i + j


def get_alpha_channel(i, j):
    return 0xFF


def get_rgba_int(r, g, b, a):
    return int(a % 256 << 24 | b % 256 << 16 | g % 256 << 8 | r % 256)


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

    def test_open_toml(self):
        data = open_toml(self.path)
        self.assertIsInstance(data, dict)

    def test_save_image_buf(self):
        image_buf = []
        path = os.path.join(os.path.dirname(__file__), "../example.png")
        with Image.open(path) as image:
            WIDTH, HEIGHT = image.size
            S_W = 7
            S_H = 7
            PIX_PER_CELL_X = WIDTH / S_W
            PIX_PER_CELL_Y = HEIGHT / S_H
            image_buf = image.getdata()
            for i in range(S_W):
                for j in range(S_H):
                    x = i * PIX_PER_CELL_X
                    y = j * PIX_PER_CELL_Y
                    w = 0.1 * PIX_PER_CELL_X
                    h = 0.4 * PIX_PER_CELL_Y
                    c = 1.0
                    draw_box(x, y, w, h, c)

        path = os.path.join(os.path.dirname(__file__), "../test.png")
        save_image_buf(image_buf, path, size=(WIDTH, HEIGHT))


if __name__ == "__main__":
    unittest.main()
