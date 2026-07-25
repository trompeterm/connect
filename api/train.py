import tqdm

# Load dataset
import torch

from data.dataset import Connect4Dataset
from torch.utils.data import random_split

dataset = Connect4Dataset("data/connect4_dataset.pt")
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train, val = random_split(dataset, [train_size, val_size])

# Create DataLoaders
from torch.utils.data import DataLoader

train_loader = DataLoader(train, batch_size=64, shuffle=True)
val_loader = DataLoader(val, batch_size=64, shuffle=False)


# Create model
from models.mlp import Connect4MLP
model = Connect4MLP()

# Create optimizer
from torch import optim
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Create loss function
from torch import nn
criterion = nn.CrossEntropyLoss()

for epoch in tqdm.tqdm(range(10)):
    model.train()
    running_loss = 0.0

    for boards, moves in train_loader:
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

    torch.save(model.state_dict(), "models/mlp.pt")
    # Training loop

    # Validation loop

    # Print loss and accuracy