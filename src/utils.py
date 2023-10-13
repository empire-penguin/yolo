import toml

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
