import argparse
import random
import torch

from game import Connect4


def canonical_board(game):
    """
    Always represent the board from the CURRENT player's perspective.
    """
    player = game.current_player

    board = [
        [cell * player for cell in row]
        for row in game.board
    ]

    return board


def winning_move(game, player):
    """
    Returns a winning column for player if one exists.
    """

    for move in game.legal_moves():
        g = game.copy()
        g.current_player = player
        g.play(move)

        if g.winner() == player:
            return move

    return None


def choose_move(game):
    player = game.current_player
    opponent = -player

    # Immediate win
    move = winning_move(game, player)
    if move is not None:
        return move

    # Block opponent
    move = winning_move(game, opponent)
    if move is not None:
        return move

    # Random
    return random.choice(game.legal_moves())


def generate(num_games):

    dataset = []

    for game_number in range(num_games):

        game = Connect4()

        while True:

            if game.winner() != 0:
                break

            if game.is_full():
                break

            board = canonical_board(game)

            move = choose_move(game)

            dataset.append(
                {
                    "board": board,
                    "move": move,
                }
            )

            game.play(move)

        if (game_number + 1) % 500 == 0:
            print(f"Generated {game_number + 1} games")

    return dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=5000)

    args = parser.parse_args()

    dataset = generate(args.games)

    torch.save(dataset, "data/connect4_dataset.pt")

    print()
    print(f"Saved {len(dataset)} positions.")


if __name__ == "__main__":
    main()