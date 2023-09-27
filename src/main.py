#!/usr/bin/env python3

import toml
import os

from src.trainer import Trainer


def parse(path):
    with open(path, "r") as f:
        data = toml.load(f)
    return data


def main(*args, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
    data = parse(path)

    BOUND_BOXES = data["arch"]["B"]
    CLASSES = data["arch"]["C"]
    GRID_CELLS = data["arch"]["S"]

    print(f"Number of bounding boxes: {BOUND_BOXES}")
    print(f"Number of classes: {CLASSES}")
    print(f"Number of grid cells: {GRID_CELLS}")

    t = Trainer(data)
    t.train()


if __name__ == "__main__":
    main()
