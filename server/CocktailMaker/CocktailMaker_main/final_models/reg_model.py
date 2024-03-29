import pandas as pd
import numpy as np
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from tqdm.auto import tqdm
from torch.optim import AdamW, SGD
from sklearn.metrics import *
from torch.optim.lr_scheduler import CosineAnnealingLR
import pickle

class MainModel(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=128):
        super().__init__()
        self.cls = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size),
            nn.Linear(hidden_size, hidden_size*2),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size*2),
            nn.Linear(hidden_size*2, hidden_size*2),
            nn.ReLU(),
            nn.BatchNorm1d(hidden_size*2),
            nn.Linear(hidden_size*2, output_size),
        )

    def forward(self, x):
        x = self.cls(x)
        return nn.Sigmoid()(x)
