import random
import math


class RandomHeuristicPlayer:
    """
    Random player that:
    1. Wins immediately if possible.
    2. Blocks opponent wins.
    3. Otherwise plays randomly.
    """

    def choose_move(self, game):

        player = game.current_player
        opponent = -player

        move = self._winning_move(game, player)
        if move is not None:
            return move

        move = self._winning_move(game, opponent)
        if move is not None:
            return move

        return random.choice(game.legal_moves())

    def _winning_move(self, game, player):

        for move in game.legal_moves():

            g = game.copy()
            g.current_player = player
            g.play(move)

            if g.winner() == player:
                return move

        return None

class AlphaBetaPlayer:
    def __init__(self, depth=3):
        self.depth = depth

    def choose_move(self, game):
        root_player = game.current_player

        best_move = None
        best_score = -math.inf

        alpha = -math.inf
        beta = math.inf

        for move in game.legal_moves():
            row = game.make_move(move)

            score = self.alphabeta(
                game,
                self.depth - 1,
                alpha,
                beta,
                False,
                root_player,
            )

            game.undo_move(row, move)

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def alphabeta(
        self,
        game,
        depth,
        alpha,
        beta,
        maximizing,
        root_player,
    ):
        winner = game.winner()

        if depth == 0 or winner != 0 or game.is_full():
            return self.evaluate(game, root_player)

        if maximizing:

            value = -math.inf

            for move in game.legal_moves():
                row = game.make_move(move)

                value = max(
                    value,
                    self.alphabeta(
                        game,
                        depth-1,
                        alpha,
                        beta,
                        False,
                        root_player,
                    ),
                )

                game.undo_move(row, move)

                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return value

        else:

            value = math.inf

            for move in game.legal_moves():
                
                row = game.make_move(move)

                value = min(
                    value,
                    self.alphabeta(
                        game,
                        depth-1,
                        alpha,
                        beta,
                        True,
                        root_player
                    )
                )
                game.undo_move(row, move)

                beta = min(beta, value)

                if beta <= alpha:
                    break

            return value

    ###########################################################
    # Evaluation
    ###########################################################

    def evaluate(self, game, player):

        winner = game.winner()

        if winner == player:
            return 1_000_000

        if winner == -player:
            return -1_000_000

        score = 0
        board = game.board

        #
        # Center column preference
        #
        center = [board[r][3] for r in range(6)]
        score += center.count(player) * 3
        score -= center.count(-player) * 3

        #
        # Horizontal
        #
        for r in range(6):
            for c in range(4):
                window = board[r][c:c + 4]
                score += self.evaluate_window(window, player)

        #
        # Vertical
        #
        for c in range(7):
            for r in range(3):
                window = [
                    board[r + i][c]
                    for i in range(4)
                ]
                score += self.evaluate_window(window, player)

        #
        # Positive diagonal
        #
        for r in range(3):
            for c in range(4):
                window = [
                    board[r + i][c + i]
                    for i in range(4)
                ]
                score += self.evaluate_window(window, player)

        #
        # Negative diagonal
        #
        for r in range(3, 6):
            for c in range(4):
                window = [
                    board[r - i][c + i]
                    for i in range(4)
                ]
                score += self.evaluate_window(window, player)

        return score

    def evaluate_window(self, window, player):

        opponent = -player

        mine = window.count(player)
        theirs = window.count(opponent)
        empty = window.count(0)

        score = 0

        #
        # My opportunities
        #
        if mine == 4:
            score += 100000

        elif mine == 3 and empty == 1:
            score += 100

        elif mine == 2 and empty == 2:
            score += 10

        elif mine == 1 and empty == 3:
            score += 1

        #
        # Opponent threats
        #
        if theirs == 4:
            score -= 100000

        elif theirs == 3 and empty == 1:
            score -= 120

        elif theirs == 2 and empty == 2:
            score -= 12

        elif theirs == 1 and empty == 3:
            score -= 1

        return score

    def score_moves(self, game):

        root_player = game.current_player

        scores = []

        for move in game.legal_moves():

            row = game.make_move(move)

            score = self.alphabeta(
            game,
            self.depth - 1,
            float("-inf"),
            float("inf"),
            False,
            root_player,
            )

            game.undo_move(row, move)

            scores.append((move, score))

        return scores