import toml
import PIL.Image as Image
import math
import numpy as np


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
    for i in range(image_buf.shape[0]):
        for j in range(image_buf.shape[1]):
            for bbox in bbox_list:
                if bbox.on_edge(i, j):
                    image_buf[i][j] = [255, 0, 0]

                if (bbox.get_top_left()[0] - i) ** 2 + (
                    bbox.get_top_left()[1] - j
                ) ** 2 < 5**2 or (bbox.get_bottom_right()[0] - i) ** 2 + (
                    bbox.get_bottom_right()[1] - j
                ) ** 2 < 5**2:
                    image_buf[i][j] = [0, 255, 0]

    return image_buf
