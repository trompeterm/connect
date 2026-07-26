import torch
from torch.utils.data import Dataset


class Connect4Dataset(Dataset):

    def __init__(self, path, transform=None):

        self.data = torch.load(path)
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        sample = self.data[idx]

        board = torch.tensor(
            sample["board"],
            dtype=torch.float32
        )

        move = torch.tensor(
            sample["move"],
            dtype=torch.long
        )

        if self.transform:
            board = self.transform(board)

        return board, move