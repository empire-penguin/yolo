import unittest
import os
import torch
from src.model import CulinaryModel
from src.utils import open_toml


class TestCulinaryModel(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), "../config/defaut.toml")
        self.config = open_toml(path)
        self.model = CulinaryModel(self.config)

    def test_forward_pass(self):
        x = torch.rand(1, 3, 448, 448)
        y = self.model.forward(x)
        self.assertEqual(y.shape, torch.Size([7,7,30]))
        

if __name__ == "__main__":
    unittest.main()
