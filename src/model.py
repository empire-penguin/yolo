import torch
import torch.nn as nn


class CulinaryModel(nn.Module):
    def __init__(self, config):
        super(CulinaryModel, self).__init__()
        self.config = config
        self.layers = self._make_layers(self.config["model"])

    def _make_layer(layer_params):
        print(layer_params)
        
    def forward(self, x):
        pass