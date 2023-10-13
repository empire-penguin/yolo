import unittest
import torch
from src.model import CulinaryModel


class TestCulinaryModel(unittest.TestCase):
    def setUp(self):
        self.config = {"input_size": 448, "num_classes": 10}
        self.model = CulinaryModel(self.config)

    def test_forward_pass(self):
        x = torch.randn(1, 3, 448, 448)
        y = self.model(x)
        self.assertEqual(y.size(), torch.Size([1, 10]))


if __name__ == "__main__":
    unittest.main()
