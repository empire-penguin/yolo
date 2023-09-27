import torch

from torch.utils.data import Dataset

import os


class CulinaryDataset(Dataset):
    def __init__(self, data_dir, label_dir, batch_size, image_size):
        self.data_dir = data_dir
        self.label_dir = label_dir
        self.batch_size = batch_size
        self.image_size = image_size
        self.images = os.listdir(self.data_dir)
        self.labels = os.listdir(self.label_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = os.path.join(self.data_dir, self.images[idx])
        label_path = os.path.join(self.label_dir, self.labels[idx])
        image = torch.load(image_path)
        label = torch.load(label_path)
        return image, label
