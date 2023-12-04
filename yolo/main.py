#! /usr/bin/env python3
import toml
import os

from model import Yolo

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), '../config/default.toml')
    config = toml.load(config_path)
    model = Yolo(config["model"])
    
    print(model.config)