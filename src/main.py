#!/usr/bin/env python3

import toml
import os

from trainer import Trainer


def parse(path):
    with open(path, "r") as f:
        data = toml.load(f)
    return data


def main(*args, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
    data = parse(path)

    t = Trainer(data)
    t.train()
    t.test()


if __name__ == "__main__":
    main()
