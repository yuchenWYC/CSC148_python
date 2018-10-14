"""Games"""

from typing import Any
from current_state import CurrentState, SubtractSquareState, ChopsticksState
from helper_function import get_start_number


class Game:
    """
    A two-player, sequential move, zero-sum and perfect-information game.

    current_state - the current situation of the game to keep track of it.
    """

    def __init__(self, p1first: bool) -> None:
        """Initialize a game, setting its current state and deciding which
        player is to make the first move using p1first.
        p1first = True - Player 1 is to make the first move
        p1first = False - Player 2 is to make the first move
        >>> g = Game(True)
        """
        if p1first:
            self._player_to_start = 'p1'
        else:
            self._player_to_start = 'p2'
        self.current_state = CurrentState(self._player_to_start)

    def get_instructions(self) -> str:
        """Return an instruction of the game"""
        raise NotImplementedError('Subclass needed!')

    def is_over(self, current_state: CurrentState) -> bool:
        """
        Return whether self is over by checking if there is still possible
        moves for the player in current_state.
        """
        return current_state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """Return whether player is the winner of game self(wether there is
        no possible moves for the opponent and the game is over)."""
        opponent = ''
        if player == 'p1':
            opponent = 'p2'
        elif player == 'p2':
            opponent = 'p1'
        return (opponent == self.current_state.get_current_player_name()
                and self.is_over(self.current_state))

    def str_to_move(self, move: str) -> object:
        """Return a move to be made in self converting from string move."""
        raise NotImplementedError('Subclass needed!')

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.
        >>> g = Game(True)
        >>> g2 = Game(False)
        >>> g3 = Game(True)
        >>> g == g2
        False
        >>> g == g3
        True
        """
        return (type(self) == type(other)
                and self.current_state == other.current_state)

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        raise NotImplementedError('Subclass needed!')


class SubtractSquare(Game):
    """Game substract Square."""
    def __init__(self, turn: bool) -> None:
        """
        Initialize a Subtract Square game, setting its current state to
        current_state in which user will be asked to enter a non-negative
        whole number to start the game.
        Extend and override Game.__init__(p1first)
        """
        Game.__init__(self, turn)
        self.current_state = SubtractSquareState(self._player_to_start,
                                                 get_start_number())

    def get_instructions(self) -> str:
        """
        Return an instruction of the game self.
        """
        return ('Players take turns subtracting square numbers from the '
                'starting number. The winner is \nthe person who subtracts '
                'to 0.')

    def str_to_move(self, move: str) -> int:
        """
        Return a move to be made in self converting from string move.
        """
        return int(move)

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        return 'Game Substract Square: {}'.format(str(self.current_state))


class Chopsticks(Game):
    """Game chopsticks."""
    def __init__(self, turn: bool) -> None:
        """
        Initialize a Chopsticks game self, setting its current state to
        current_state in which both players have one finger pointing up
        on each hand.
        Extend and override Game.__init__(p1first)
        >>> c = Chopsticks(True)
        >>> print(c.current_state)
        Player 1: 1 - 1; Player 2: 1 - 1
        """
        Game.__init__(self, turn)
        self.current_state = ChopsticksState(self._player_to_start,
                                             (1, 1), (1, 1))

    def str_to_move(self, move: str) -> str:
        """
        Return a move to be made in self converting from string move.
        >>> c = Chopsticks(True)
        >>> c.str_to_move('ll')
        'll'
        """
        return move

    def get_instructions(self) -> str:
        """
        Return an instruction of self.
        >>> c = Chopsticks(True)
        >>> c.get_instructions()[:59]
        'Players take turns adding the values of one of their hands '
        """
        return ("Players take turns adding the values of one of their hands "
                "to one of their opponents\n(modulo 5). A hand with a total "
                "of 5 (or 0; 5 modulo 5) is considered \'dead\'. The fir\nst "
                "player to have 2 dead hands is the loser.")

    def __str__(self) -> str:
        """
        Return a string representation of self.
        >>> c = Chopsticks(True)
        >>> print(c)
        Game Chopsticks: Player 1: 1 - 1; Player 2: 1 - 1
        """
        return 'Game Chopsticks: {}'.format(str(self.current_state))


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
