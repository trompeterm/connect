import torch


class FlattenBoard:
    """
    6x7 -> 42
    """

    def __call__(self, board):
        return board.flatten()


class CNNBoard:
    """
    6x7 ->
    2x6x7

    channel 0 = player 1 pieces
    channel 1 = player 2 pieces
    """

    def __call__(self, board):
        current = (board == 1).float()
        opponent = (board == -1).float()

        return torch.stack([current, opponent], dim=0)