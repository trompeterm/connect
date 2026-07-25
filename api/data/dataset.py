import torch
from torch.utils.data import Dataset


class Connect4Dataset(Dataset):
    def __init__(self, path):
        self.data = torch.load(path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]

        board = sample["board"]
        move = sample["move"]

        # Ensure tensors
        board = torch.tensor(board, dtype=torch.float32)
        move = torch.tensor(move, dtype=torch.long)

        return board, move