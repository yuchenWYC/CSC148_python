"""a"""
from unittest.mock import patch
from game_interface import playable_games, usable_strategies
from strategy import Box, add_child
from copy import deepcopy
from typing import Any
from game import Game
minimax_iterative_strategy = usable_strategies['mi']
minimax_recursive_strategy = usable_strategies['mr']
StonehengeGame = playable_games['h']
SubtractSquareGame = playable_games['s']

STONEHENGE_MINIMAX_BOARD = """\
          2   1
         /   /
    1 - 1 - 1   @
       / \\ / \\ /
  1 - 2 - 1 - 1   2
     / \\ / \\ / \\ /
2 - 2 - 2 - H - 2
     \\ / \\ / \\ / \\
  @ - J - 2 - L   1
       \\   \\   \\
        2   2   1
"""


def iterative_strategy_test(game: Game) -> Any:
    """
    Return a move for game that produces a "highest guaranteed score" at each
    step for the current player using stack and a tree structure.
    """
    s = Stack()
    root = Box(game.current_state)
    s.add(root)
    game0 = deepcopy(game)
    while not s.is_empty():
        cur = s.remove()
        if game0.is_over(cur.state):
            player = cur.state.get_current_player_name()
            opponent = 'p1' if player == 'p2' else 'p2'
            game0.current_state = cur.state
            if game0.is_winner(player):
                cur.highest_score = 1
            elif game0.is_winner(opponent):
                cur.highest_score = -1
            else:
                cur.highest_score = 0
        else:
            if cur.children == []:
                s.add(cur)
                add_child(cur, s, game)
            else:
                cur.highest_score = max([-1 * child.highest_score
                                         for child in cur.children])
    good_moves = []
    move_dict = {}
    for child in root.children:
        if child.highest_score == -1 * root.highest_score:
            good_moves.append(child.move)
        move_dict[child.move] = child.highest_score

    print(move_dict)


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.
        """
        self._storage = []

    def add(self, obj: object)-> None:
        """ Add object obj to top of Stack self.
        """
        self._storage.append(obj)

    def remove(self) -> Box:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty, otherwise
        raises EmptyStackException
        >>> s = Stack()
        >>> s.add(5)
        >>> s.add(7)
        >>> s.remove()
        7
        """
        if self.is_empty():
            raise Exception('Empty container!')
        else:
            return self._storage.pop()

    def is_empty(self) -> bool:
        """
        Return whether Stack self is empty.
        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add(s)
        >>> s.is_empty()
        False
        """
        return len(self._storage) == 0

if __name__ == "__main__":
    with patch('builtins.input', return_value='23'):
        game = SubtractSquareGame(True)

    move_chosen1 = iterative_strategy_test(game)
    # expected_moves = [game.str_to_move("1"), game.str_to_move("16")]
    # print(move_chosen in expected_moves)
