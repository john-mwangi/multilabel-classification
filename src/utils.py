"""
This module contains utilities for calculating the loss function,
handling categorical variables.
"""

from typing import final
import torch
import torch.nn as nn
import pandas as pd


class MoaDataset:
    def __init__(self, dataset, targets) -> None:
        self.dataset = dataset
        self.targets = targets

    def __len__(self):
        return self.dataset.shape[0]

    # Given a key, returns a row containing the features and targets
    # associated with the key
    def __getitem__(self, item):
        return {
            "X": torch.tensor(data=self.dataset[item, :], dtype=torch.float),
            "y": torch.tensor(data=self.targets[item, :], dtype=torch.float)
        }


# Defining a class for actual training
class Engine:
    def __init__(self, model, optimizer, device) -> None:
        self.model = model
        self.optimizer = optimizer
        self.device = device

    def loss_fn(self, targets, outputs):
        return nn.BCEWithLogitsLoss()(outputs, targets)

    def train_loss(self, data_loader):

        self.model.train()
        final_loss = 0

        for batch in data_loader:
            self.optimizer.zero_grad()
            inputs = batch["X"].to(self.device)
            targets = batch["y"].to(self.device)
            outputs = self.model(inputs)
            loss = self.loss_fn(targets=targets, outputs=outputs)
            loss.backward()
            self.optimizer.step()
            final_loss += loss.item()

        # Return the average loss
        return final_loss/len(data_loader)

    def eval_loss(self, data_loader):

        self.model.eval()
        final_loss = 0

        for batch in data_loader:
            inputs = batch["X"].to(self.device)
            targets = batch["y"].to(self.device)
            outputs = self.model(inputs)
            loss = self.loss_fn(targets=targets, outputs=outputs)
            final_loss += loss.item()

        return final_loss / len(data_loader)

    def add_dummies(data, columns):

        ohe = pd.get_dummies(data=data[columns])
        data = data.drop(columns, axis=1)
        data = data.join(ohe)

        return data

    def process_data(df):

        df = df.drop(labels="sig_id", axis=1)
        cat_features = df.select_dtypes(include="object").columns
        df = add_dummies(data=df, columns=cat_features)
        return df

