# module to train a model\

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from src.dataset import CulinaryDataset
from src.model import CulinaryModel

from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

import os
import time


class Trainer:
    def __init__(self, config):
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = CulinaryModel().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config["lr"])
        self.criterion = nn.MSELoss()
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, patience=3, verbose=True
        )
        self.writer = SummaryWriter(
            os.path.join(self.config["log_dir"], time.strftime("%Y-%m-%d-%H-%M-%S"))
        )
        self.train_dataset = CulinaryDataset(
            self.config["train"]["data_dir"],
            self.config["train"]["label_dir"],
            self.config["train"]["batch_size"],
            self.config["train"]["image_size"],
        )
        self.val_dataset = CulinaryDataset(
            self.config["val"]["data_dir"],
            self.config["val"]["label_dir"],
            self.config["val"]["batch_size"],
            self.config["val"]["image_size"],
        )
        self.train_dataloader = DataLoader(
            self.train_dataset,
            batch_size=self.config["train"]["batch_size"],
            shuffle=self.config["train"]["shuffle"],
            num_workers=self.config["train"]["num_workers"],
        )
        self.val_dataloader = DataLoader(
            self.val_dataset,
            batch_size=self.config["val"]["batch_size"],
            shuffle=self.config["val"]["shuffle"],
            num_workers=self.config["val"]["num_workers"],
        )

    def train(self):
        for epoch in range(self.config["epochs"]):
            self.model.train()
            running_loss = 0.0
            for i, data in enumerate(self.train_dataloader):
                images, labels = data
                images = images.to(self.device)
                labels = labels.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
                if i % 100 == 99:
                    self.writer.add_scalar(
                        "training loss",
                        running_loss / 100,
                        epoch * len(self.train_dataloader) + i,
                    )
                    running_loss = 0.0
            self.scheduler.step(running_loss)
            self.writer.add_scalar(
                "learning rate", self.optimizer.param_groups[0]["lr"], epoch
            )
            self.validate(epoch)

    def validate(self, epoch):
        self.model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for i, data in enumerate(self.val_dataloader):
                images, labels = data
                images = images.to(self.device)
                labels = labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                running_loss += loss.item()
                if i % 100 == 99:
                    self.writer.add_scalar(
                        "validation loss",
                        running_loss / 100,
                        epoch * len(self.val_dataloader) + i,
                    )
                    running_loss = 0.0
        self.writer.flush()
        torch.save(
            self.model.state_dict(), os.path.join(self.config["log_dir"], "model.pth")
        )

    def test(self):
        pass

    def predict(self):
        pass

    def evaluate(self):
        pass

    def save(self):
        pass

    def load(self):
        pass
