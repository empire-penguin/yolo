import unittest
import os
import numpy as np
import math

import PIL.Image as Image

import sys

sys.path.append(".")

from src.utils import (
    open_toml,
    draw_bbox_on_image,
    generate_grid_cells,
    draw_grid_on_image,
)
from src.bbox import BoundingBox


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
        self.width = 500
        self.height = 375
        self.bbox1 = BoundingBox(143, 178, 48, 124, 0.1)
        self.bbox2 = BoundingBox(338, 236, 297, 241, 0.1)
        self.bbox3 = BoundingBox(62, 178, 48, 124, 0.1)
        self.bbox4 = BoundingBox(100, 47, 167, 65, 0.1)

    def test_open_toml(self):
        data = open_toml(self.path)
        self.assertIsInstance(data, dict)

    def test_draw_bboxes_on_image(self):
        with open(
            os.path.join(os.path.dirname(__file__), "../images/example.jpg"), "rb"
        ) as f:
            image_buf = np.array(Image.open(f))

        image_buf = draw_bbox_on_image(
            image_buf,
            [self.bbox1, self.bbox2, self.bbox3, self.bbox4],
        )
        image = Image.fromarray(image_buf, "RGB")
        image.save("images/test.png")

    def test_generate_grid(self):
        grids = generate_grid_cells((450, 513), (7, 8))
        assert grids.shape == (7, 8)
        total_pixels = 450 * 513
        count = 0
        for i in range(7):
            for j in range(8):
                count += grids[i][j].width * grids[i][j].height

        assert count == total_pixels

    def test_draw_grid_on_image(self):
        with open(
            os.path.join(os.path.dirname(__file__), "../images/example.jpg"), "rb"
        ) as f:
            image_buf = np.array(Image.open(f))

        grids = generate_grid_cells((image_buf.shape[1], image_buf.shape[0]), (7, 7))
        print(grids)
        image_buf = draw_grid_on_image(
            image_buf,
            grids,
        )
        image = Image.fromarray(image_buf, "RGB")
        image.save("images/test.png")


if __name__ == "__main__":
    unittest.main()
