# module to train a model\

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# from dataset import CulinaryDataset
from model import CulinaryModel

from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets, transforms

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

        # Define the data transformations
        transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )

        # Define the train dataloader
        self.train_dataloader = DataLoader(
            datasets.VOCDetection(
                root="dataset",
                year="2012",
                image_set="train",
                transform=transform,
            ),
            batch_size=self.config["batch_size"],
            shuffle=self.config["shuffle"],
            num_workers=self.config["num_workers"],
        )

        # Define the validate dataloader
        self.val_dataloader = DataLoader(
            datasets.VOCDetection(
                root="dataset",
                year="2012",
                image_set="val",
                transform=transform,
            ),
            batch_size=self.config["batch_size"],
            shuffle=self.config["shuffle"],
            num_workers=self.config["num_workers"],
        )

    def train(self):
        for epoch in range(self.config["epochs"]):
            self.train_epoch(epoch)
            self.validate(epoch)
        self.save()

    def train_epoch(self, epoch):
        self.model.train()
        running_loss = 0.0
        for images, targets in self.train_dataloader:
            for target in targets:
                # Extract bounding box coordinates
                boxes = target["annotation"]["object"]["bndbox"]
                # Extract object label
                label = target["annotation"]["object"]["name"]

            images, targets = images.to(self.device), targets.to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()
            running_loss += loss.item() * images.size(0)
        self.writer.add_scalar("Loss/train", running_loss, epoch)
        self.scheduler.step(running_loss)

    def validate(self, epoch):
        self.model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for images, targets in self.val_dataloader:
                images, targets = images.to(self.device), targets.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, targets)
                running_loss += loss.item() * images.size(0)
        self.writer.add_scalar("Loss/val", running_loss, epoch)

    def test(self):
        self.load()
        pass

    def save(self):
        torch.save(
            self.model.state_dict(), os.path.join(self.config["log_dir"], "model.pth")
        )

    def load(self):
        torch.load(
            self.model.state_dict(), os.path.join(self.config["log_dir"], "model.pth")
        )
