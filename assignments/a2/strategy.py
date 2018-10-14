"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from random import randint
from copy import deepcopy
from game import Game
from game_state import GameState

# TODO: Adjust the type annotation as needed.


def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)


def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2  # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move


def recursive_strategy(game: Game) -> Any:
    """
    Return a move for game that produces a "highest guaranteed score" at each
    step for the current player using recursion.
    """
    # player = game.current_state.get_current_player_name()
    # opponent = 'p1' if player == 'p2' else 'p2'
    score_dict = get_score(game)
    # recursion is used in helper function get_score
    move = ''
    if score_dict[1] != [] and score_dict[1] != ['over']:
        move = choose_random_move(score_dict[1])
    elif score_dict[0] != [] and score_dict[0] != ['over']:
        move = choose_random_move(score_dict[0])
    elif score_dict[-1] != [] and score_dict[-1] != ['over']:
        move = choose_random_move(score_dict[-1])
    return game.str_to_move(str(move))


def get_score(game: Game) -> dict:
    """
    Return a score of the game's current state, either '-1', '0' or '1',
    using recursion.
    """
    score_dict = {-1: [], 0: [], 1: []}
    if game.is_over(game.current_state):
        player = game.current_state.get_current_player_name()
        opponent = 'p1' if player == 'p2' else 'p2'  # revised here after due :(
        if game.is_winner(player):
            score = 1
        elif game.is_winner(opponent):
            score = -1
        else:
            score = 0
        score_dict[score].append('over')
    else:
        moves = game.current_state.get_possible_moves()
        for move in moves:
            move_to_make = game.str_to_move(str(move))
            game_copy = deepcopy(game)
            game_copy.current_state = game.current_state.make_move(move_to_make)
            next_score_dict = get_score(game_copy)
            oppo_score = -1000  # some invalid number at this point
            if next_score_dict[1] != []:
                oppo_score = 1
            elif next_score_dict[0] != []:
                oppo_score = 0
            elif next_score_dict[-1] != []:
                oppo_score = -1
            score_dict[-1 * oppo_score].append(move)
    return score_dict


def choose_random_move(score_list: list) -> str:
    """
    Return a move randomly chosen from moves that the new position has the same
    score.
    >>> score_list0 = ['1', '4', '9']
    >>> expect_list0 = ['1', '4', '9']
    >>> print(choose_random_move(score_list0) in expect_list0)
    True
    >>> score_list1 = ['1', '4', 'over']
    >>> expect_list1 = ['1', '4']
    >>> print(choose_random_move(score_list1) in expect_list1)
    True
    """
    index = randint(0, len(score_list) - 1)
    move = score_list[index]
    while move == 'over':
        move = score_list[index]
    return move


def iterative_strategy(game: Game) -> Any:
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
    good_moves = [child.move for child in root.children
                  if child.highest_score == -1 * root.highest_score]
    index = randint(0, len(good_moves) - 1)
    return game.str_to_move(str(good_moves[index]))


class Box:
    """
    A class holding GameState, the move that leads to this state from the
    previous one, its children and its highest guaranteed score.
    """
    def __init__(self, state: GameState, move=None, children=None,
                 highest_score=None) -> None:
        """
        Inistialize a box self, holding state, move, children and
        highest_score.
        """
        self.state = state
        self.children = [] if children is None else children[:]
        self.highest_score = highest_score
        self.move = move

    def __str__(self) -> str:
        """
        return a string representation of self.
        """
        r = '[{}; {}; {}; {}]'
        return r.format(self.state, self.move, self.children,
                        self.highest_score)


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


def add_child(cur: Box, s: Stack, game: Game) -> None:
    """
    Add every possible move for cur.state as a child to cur.children as well
    as to the top of s.
    """
    moves = cur.state.get_possible_moves()
    for move in moves:
        next_state = \
            cur.state.make_move(game.str_to_move(str(move)))
        child = Box(next_state, move)
        cur.children.append(child)
        s.add(child)


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
