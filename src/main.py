#!/usr/bin/env python3

import os
from trainer import Trainer
from utils import parse


def main(*args, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
    data = parse(path)

    t = Trainer(data)
    t.train()
    t.test()


if __name__ == "__main__":
    main()
