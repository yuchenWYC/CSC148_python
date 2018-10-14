"""strategies for player in game_interface"""

from game1 import Game


def interactive_strategy(game: Game) -> object:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def random_strategy(game: Game) -> object:
    """
    Return a move for game through random choosing from possible moves.
    """
    move = game.current_state.choose_random_move()
    return game.str_to_move(move)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
