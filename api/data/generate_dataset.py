import argparse
import torch
import random
from game.board import Connect4
from game.players import RandomHeuristicPlayer, AlphaBetaPlayer


def canonical_board(game):
    player = game.current_player

    return [
        [cell * player for cell in row]
        for row in game.board
    ]


def generate(num_games):

    player = AlphaBetaPlayer()

    dataset = []

    for game_number in range(num_games):

        game = Connect4()

        while not game.is_full() and game.winner() == 0:

            board = canonical_board(game)
            scored_moves = player.score_moves(game)
            best_score = max(score for _, score in scored_moves)
            candidate_moves = [
                move
                for move, score in scored_moves
                if score >= best_score - 10
            ]

            move = random.choice(candidate_moves)

            dataset.append({
                "board": board,
                "move": move,
            })

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

    print(f"Saved {len(dataset)} positions.")


if __name__ == "__main__":
    main()