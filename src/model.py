import torch
import torch.nn as nn


class CulinaryModel(nn.Module):
    def __init__(self, config):
        super(CulinaryModel, self).__init__()
        self.config = config
        self.layers = self._make_layers(self.config["model"]["layers"])

    def _make_layers(self, layers_params):
        for layer_p in layers_params:
            pass

    def forward(self, x):
        return torch.rand(7, 7, 30)
