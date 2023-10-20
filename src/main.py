#!/usr/bin/env python3

import os
from trainer import Trainer
from utils import open_toml


def main(*args, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
    data = open_toml(path)

    t = Trainer(data)
    t.train()
    t.test()


if __name__ == "__main__":
    main()
