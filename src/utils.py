import toml
import PIL.Image as Image
import math


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
