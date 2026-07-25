import copy

ROWS = 6
COLS = 7


class Connect4:
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = -1

    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = self.PLAYER1

    def copy(self):
        return copy.deepcopy(self)

    def legal_moves(self):
        return [c for c in range(COLS) if self.board[0][c] == 0]

    def play(self, col):
        if col not in self.legal_moves():
            return False

        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player *= -1
                return True

        return False

    def is_full(self):
        return len(self.legal_moves()) == 0

    def winner(self):
        b = self.board

        directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ]

        for r in range(ROWS):
            for c in range(COLS):
                if b[r][c] == 0:
                    continue

                player = b[r][c]

                for dr, dc in directions:
                    count = 0

                    for i in range(4):
                        rr = r + dr * i
                        cc = c + dc * i

                        if (
                            0 <= rr < ROWS
                            and 0 <= cc < COLS
                            and b[rr][cc] == player
                        ):
                            count += 1

                    if count == 4:
                        return player

        return 0