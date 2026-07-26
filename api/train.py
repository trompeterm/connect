import argparse
import random
import numpy as np
import torch

from torch import nn, optim
from torch.utils.data import DataLoader, random_split

from data.dataset import Connect4Dataset
from data.transforms import FlattenBoard, CNNBoard
from models import get_model

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model",
        type=str,
        required=True
    )

    parser.add_argument(
        "--epochs",
        type=int,
    )

    parser.add_argument(
        "--batch_size",
        type=int,
    )

    parser.add_argument(
        "--learning_rate",
        type=float,
    )

    return parser.parse_args()

args = parse_args()

NUM_EPOCHS = args.epochs
BATCH_SIZE = args.batch_size
LEARNING_RATE = args.learning_rate

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = args.model.lower()
if model_name == "mlp":
    transform = FlattenBoard()
elif model_name == "cnn":
    transform = CNNBoard()
else:
    raise ValueError("Invalid model name")

dataset = Connect4Dataset("data/connect4_dataset.pt", transform=transform)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train, val = random_split(dataset, [train_size, val_size])


train_loader = DataLoader(train, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val, batch_size=BATCH_SIZE, shuffle=False)

# Create model
model = get_model(model_name).to(device)

# Create optimizer
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Create loss function
criterion = nn.CrossEntropyLoss()

best_val_loss = float("inf")

for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0

    for boards, moves in train_loader:
        boards = boards.to(device)
        moves = moves.to(device)

        optimizer.zero_grad()
        outputs = model(boards)
        loss = criterion(outputs, moves)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    model.eval()

    correct = 0
    total = 0
    val_loss = 0.0

    with torch.no_grad():
        for boards, moves in val_loader:
            boards = boards.to(device)
            moves = moves.to(device)

            outputs = model(boards)
            loss = criterion(outputs, moves)
            val_loss += loss.item()

            predictions = outputs.argmax(dim=1)
            correct += (predictions == moves).sum().item()
            total += moves.size(0)

    train_loss = running_loss / len(train_loader)
    val_loss = val_loss / len(val_loader)
    accuracy = correct / total

    print(
        f"epoch: {epoch + 1}\n", 
        f"train_loss: {train_loss:.4f}\n",
        f"val_loss: {val_loss:.4f}\n",
        f"accuracy: {accuracy:.4f}\n"
    )

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(
            model.state_dict(),
            "models/best.pt"
        )