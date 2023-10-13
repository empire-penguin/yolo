import torch
import torch.nn as nn


class CulinaryModel(nn.Module):
    def __init__(self, config):
        super(CulinaryModel, self).__init__()
        self.config = config
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3)

    def _make_layer(layer_params):
        