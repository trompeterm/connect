import torch.nn as nn

class Connect4CNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv2d(2, 64, kernel_size=3, padding=1),
            nn.ReLU(),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),

            nn.Flatten(),

            nn.Linear(128 * 6 * 7, 256),
            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(256, 7)
        )

    def forward(self, x):
        return self.net(x)