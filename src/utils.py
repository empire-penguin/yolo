import toml
import PIL.Image as Image
import math
import numpy as np
from gridcell import GridCell


def open_toml(path):
    """returns a dict from a toml file

    Args:
        path (str): path to toml file

    Returns:
        dict: dict from toml file
    """
    with open(path, "r") as f:
        data = toml.load(f)
    return data


def save_image_buf(image_buf, path, size=(448, 448, 3)):
    """saves an image buffer to a file

    Args:
        image_buf (bytes): image buffer
        path (str): path to save image to
        size (tuple, optional): size of image. Defaults to (448, 448, 3).

    Returns:
        None
    """
    image = Image.new("RGBA", size)
    image.putdata(image_buf)
    image.save(path)


def get_rgba_int(r, g, b, a):
    return int(a % 256 << 24 | b % 256 << 16 | g % 256 << 8 | r % 256)


def draw_bbox_on_image(image_buf, bbox_list):
    """Draws bounding boxes on an image buffer.

    Args:
        image_buf (numpy.ndarray): Image buffer as a NumPy array.
        bbox_list (list): List of bounding boxes.
        size (tuple, optional): Size of image. Defaults to (448, 448, 3).

    Returns:
        numpy.ndarray: Modified image buffer as a NumPy array.
    """

    for i in range(image_buf.shape[1]):
        for j in range(image_buf.shape[0]):
            for bbox in bbox_list:
                delta = math.floor(
                    0.25 * (1 - math.exp(-abs(bbox.c))) * math.log(bbox.w * bbox.h) ** 2
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


def generate_grid_cells(image_size, grid_size):
    """Generates grid cells for an image.

    Args:
        image_size (tuple): Size of image.
        grid_size (tuple): Size of grid.

    Returns:
        list: List of grid cells.
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


def draw_grid_on_image(image_buf, grid_cells):
    """Draws grid cells on an image buffer.

    Args:
        image_buf (numpy.ndarray): Image buffer as a NumPy array.
        grid_cells (list): List of grid cells.

    Returns:
        numpy.ndarray: Modified image buffer as a NumPy array.
    """

    for i in range(grid_cells.shape[0]):
        for j in range(grid_cells.shape[1]):
            image_buf = draw_bbox_on_image(image_buf, grid_cells[i][j].get_bbox_list())

    return image_buf
