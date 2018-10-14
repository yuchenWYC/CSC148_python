"""
A module of game_interface. Complete the "TODOs" and reason about what
classes you need to design to make this interface work.
"""
from typing import Callable, Union
from strategy1 import random_strategy, interactive_strategy
from game1 import Game, SubtractSquare, Chopsticks

# 's' should map to your implementation of Subtract Square, and 'c' should map
# to Chopsticks.
playable_games = {'s': SubtractSquare,
                  'c': Chopsticks}

# The strategies you are to implement.  See strategy.py, and then decide
# how to modify this.
usable_strategies = {'r': random_strategy,
                     'i': interactive_strategy}


class GameInterface:
    """
    A game interface for a two-player, sequential move, zero-sum,
    perfect-information game.

    game - the  game to be played
    p1_strategy - strategy for player 1
    p2_strategy - strategy for player 2
    """
    game: Game
    p1_strategy: Callable[[Game], str]
    p2_strategy: Callable[[Game], str]

    def __init__(self, game: Game,
                 p1_strategy: Callable[[Game], object],
                 p2_strategy: Callable[[Game], object]) -> None:
        """
        Initialize this GameInterface, setting its active game to game, and
        using the strategies p1_strategy for Player 1 and p2_strategy for
        Player 2.
        """
        first_player = input("Type y if player 1 is to make the first move: ")
        is_p1_turn = False
        if first_player.lower() == 'y':
            is_p1_turn = True

        self.game = game(is_p1_turn)
        self.p1_strategy = p1_strategy
        self.p2_strategy = p2_strategy

    def play(self) -> None:
        """
        Play the game.
        """
        current_state = self.game.current_state

        print(self.game.get_instructions())
        print(current_state)

        # Pick moves until the game is over
        while not self.game.is_over(current_state):
            move_to_make = None

            # Print out all of the valid moves
            possible_moves = current_state.get_possible_moves()
            print("The current available moves are:")
            for move in possible_moves:
                print(move)

            # Pick a (legal) move.
            while not current_state.is_valid_move(move_to_make):
                current_strategy = self.p2_strategy
                if current_state.get_current_player_name() == 'p1':
                    current_strategy = self.p1_strategy
                move_to_make = current_strategy(self.game)

            # Apply the move
            current_player_name = current_state.get_current_player_name()
            new_game_state = current_state.make_move(move_to_make)
            self.game.current_state = new_game_state
            current_state = self.game.current_state

            print("{} made the move {}. The game's state is now:".format(
                current_player_name, move_to_make))
            print(current_state)

        # Print out the winner of the game
        if self.game.is_winner("p1"):
            print("Player 1 is the winner!")
        elif self.game.is_winner("p2"):
            print("Player 2 is the winner!")
        else:
            print("It's a tie!")

    def __eq__(self, other):
        """Return whether self is equivalent to other."""
        return (type(self) == type(other)
                and self.game == other.game
                and self.p1_strategy == other.p1_strategy
                and self.p2_strategy == other.p2_strategy)

    def __str__(self):
        """Return a string representation of self."""
        return "Game interface with game {}, players {} and {}".format(
            self.game, self.p1_strategy, self.p2_strategy)


if __name__ == '__main__':
    games = ", ".join(["'{}': {}".format(key, playable_games[key].__name__) if
                       playable_games[key] is not None else
                       "'{}': None".format(key) for key in playable_games])

    strategies = ", ".join(["'{}': {}".format(key,
                                              usable_strategies[key].__name__)
                            if usable_strategies[key] is not None else
                            "'{}': None".format(key)
                            for key in usable_strategies])

    chosen_game = ''
    while chosen_game not in playable_games.keys():
        chosen_game = input(
            "Select the game you want to play ({}): ".format(games))

    p1 = ''
    p2 = ''

    while p1 not in usable_strategies.keys():
        p1 = input("Select the strategy for Player 1 ({}): ".format(strategies))

    while p2 not in usable_strategies.keys():
        p2 = input("Select the strategy for Player 2 ({}): ".format(strategies))

    GameInterface(playable_games[chosen_game], usable_strategies[p1],
                  usable_strategies[p2]).play()
