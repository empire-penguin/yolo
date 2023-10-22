import toml
import PIL.Image as Image
import math
import numpy as np
from yolo.gridcell import GridCell


class Utils:
    def open_toml(self, path):
        """Returns a dict with the contents of the toml file

        :returns: a dict from a toml file
        :rtype: dict
        """
        with open(path, "r") as f:
            data = toml.load(f)
        return data

    def save_image_buf(self, image_buf, path, size=(448, 448, 3)):
        """saves an image buffer to a file

        :param image_buf: image buffer as a numpy array
        :type image_buf: numpy.ndarray
        :param path: path to save the image to
        :type path: str
        :param size: size of the image, defaults to (448, 448, 3)
        :type size: tuple, optional

        :returns: None
        :rtype: None
        """
        image = Image.new("RGBA", size)
        image.putdata(image_buf)
        image.save(path)

    def get_rgba_int(self, r, g, b, a):
        return int(a % 256 << 24 | b % 256 << 16 | g % 256 << 8 | r % 256)

    def draw_bbox_on_image(self, image_buf, bbox_list):
        """Draws bounding boxes on an image buffer.

        :param image_buf: image buffer as a numpy array
        :type image_buf: numpy.ndarray
        :param bbox_list: list of bounding boxes
        :type bbox_list: list[:class:`BoundingBox`]

        :returns: modified image buffer as a numpy array
        :rtype: numpy.ndarray
        """

        for i in range(image_buf.shape[1]):
            for j in range(image_buf.shape[0]):
                for bbox in bbox_list:
                    delta = math.floor(
                        0.25
                        * (1 - math.exp(-abs(bbox.c)))
                        * math.log(bbox.w * bbox.h) ** 2
                    )
                    if bbox.on_edge(i, j, delta):
                        image_buf[j][i] = [255, 0, 255]

                    if (
                        math.floor(bbox.get_top_left()[0] - i) ** 2
                        + math.floor(bbox.get_top_left()[1] - j) ** 2
                        < 1**2
                        or math.floor(bbox.get_bottom_right()[0] - i) ** 2
                        + math.floor(bbox.get_bottom_right()[1] - j) ** 2
                        < 1**2
                        or math.floor(bbox.get_center()[0] - i) ** 2
                        + math.floor(bbox.get_center()[1] - j) ** 2
                        < 1**2
                    ):
                        image_buf[j][i] = [0, 255, 255]

        return image_buf

    def generate_grid_cells(self, image_size, grid_size):
        """Generates grid cells for an image.

        :param image_size: size of the image
        :type image_size: tuple (int, int)
        :param grid_size: size of the grid
        :type grid_size: tuple (int, int)

        :returns: list of grid cells
        :rtype: list[:class:`GridCell`]
        """
        grid_cells = np.empty(grid_size, dtype=GridCell)

        delta_w = image_size[0] // grid_size[0]
        delta_h = image_size[1] // grid_size[1]

        # Add extra pixels to last grid cells if
        # image size dimention is not divisible by grid size
        extra_w = image_size[0] % grid_size[0]
        extra_h = image_size[1] % grid_size[1]

        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                w = delta_w
                h = delta_h
                if i == grid_size[0] - 1:
                    w = delta_w + extra_w
                if j == grid_size[1] - 1:
                    h = delta_h + extra_h
                cell = GridCell(w, h, i, j)
                grid_cells[i][j] = cell

        return grid_cells

    def draw_grid_on_image(self, image_buf, grid_cells):
        """Draws grid cells on an image buffer.

        :param image_buf: image buffer as a numpy array
        :type image_buf: numpy.ndarray
        :param grid_cells: list of grid cells
        :type grid_cells: list[:class:`GridCell`]

        :returns: modified image buffer as a numpy array
        :rtype: numpy.ndarray
        """
        for i in range(grid_cells.shape[0]):
            for j in range(grid_cells.shape[1]):
                cell = grid_cells[i][j]
                print(cell)
                print(i * cell.width, j * cell.height)
                image_buf[:, i * cell.width] = [127, 127, 127]
                image_buf[j * cell.height, :] = [127, 127, 127]
                image_buf[:, i * cell.width] = [127, 127, 127]
                image_buf[j * cell.height, :] = [127, 127, 127]

                image_buf = self.draw_bbox_on_image(
                    image_buf, grid_cells[i][j].get_bbox_list()
                )

        return image_buf
