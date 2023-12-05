import torch
import torch.nn as nn
import torch.nn.functional as F


class Yolo(nn.Module):
    def __init__(self, config):
        super(Yolo, self).__init__()
        self.config = config
