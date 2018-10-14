"""current_state"""

from typing import List, Any, Tuple
import random


class CurrentState:
    """the current situation of a game to keep track of it."""
    def __init__(self, player: str) -> None:
        """
        Initialize a CurrentState self for a Game.
        >>> c = CurrentState('p1')
        """
        self._player = player

    def get_possible_moves(self) -> list:
        """Return all possible moves for the current player."""
        raise NotImplementedError('Subclass needed!')

    def is_valid_move(self, move_to_make: object) -> bool:
        """
        Return True iff move_to_make is a valid move for the current player.
        """
        return (move_to_make is not None
                and move_to_make in self.get_possible_moves())

    def get_current_player_name(self) -> str:
        """
        Return the current player, who is taking the turn.
        >>> c = CurrentState('p1')
        >>> c.get_current_player_name()
        'p1'
        """
        return self._player

    def make_move(self, move_to_make: object) -> 'CurrentState':
        """Create a new instance with new attributes provided by move_to_make
         as a snapshot of a game."""
        raise NotImplementedError('Subclass needed!')

    def choose_random_move(self) -> object:
        """Return a move randomly chosen from possible moves."""
        candidates = self.get_possible_moves()
        return random.choice(candidates)

    def __eq__(self, other: Any) -> bool:
        """
        Return whether self is equivalent to other.
        >>> c = CurrentState('p1')
        >>> c2 = CurrentState('p2')
        >>> c3 = int(3)
        >>> c4 = CurrentState('p1')
        >>> c == c2
        False
        >>> c == c3
        False
        >>> c == c4
        True
        """
        return type(self) == type(other) and self._player == other._player

    def __str__(self):
        """Return a string representation of self."""
        raise NotImplementedError('Subclass needed!')


class SubtractSquareState(CurrentState):
    """the current situation of a Substract Square game to keep track of it."""
    def __init__(self, player_to_start: str, number: int) -> None:
        """
        Initialize a SubtractSquareState self for a Substract Square game.
        >>> s = SubtractSquareState('p1', 5)
        >>> s.number
        5
        """
        CurrentState.__init__(self, player_to_start)
        self.number = number

    def get_possible_moves(self) -> List[int]:
        """
        Return all possible moves for the current player.
        >>> s = SubtractSquareState('p1', 5)
        >>> s.get_possible_moves()
        [1, 4]
        """
        return [num ** 2 for num in range(1, int(self.number ** 0.5) + 10)
                if num ** 2 <= self.number]

    def make_move(self, move_to_make: int) -> 'SubtractSquareState':
        """
        Create a new SubtractSquareState to keep track of the game.
        In the new state, the number is self.number subtract move_to_make and
        the player is different from self._player.
        >>> s = SubtractSquareState('p1', 5)
        >>> s.make_move(2).number
        3
        """
        new_number = self.number - move_to_make
        if self.get_current_player_name() == 'p1':
            next_player = 'p2'
        else:
            next_player = 'p1'
        new_state = SubtractSquareState(next_player, new_number)
        return new_state

    def __str__(self) -> str:
        """
        Return a string representation of self.
        >>> s = SubtractSquareState('p1', 5)
        >>> str(s)
        'The current value is: 5'
        """
        return "The current value is: {}".format(self.number)


class ChopsticksState(CurrentState):
    """
    the current situation of a Chopsticks game to keep track of it.
    p1 - player 1's fingers on left and right hand, each has at least 1 and at
    most 5 fingers.
    p2 - player 2's fingers on left and right hand, each has at least 1 and at
    most 5 fingers.
    """

    def __init__(self, player: str,
                 p1: Tuple[int, int], p2: Tuple[int, int]) -> None:
        """
        Initialize a ChopsticksState self for a Chopsticks game.
        Each of two players begins with one nger pointed up on each of
        their hands.
        >>> c = ChopsticksState('p1', (1, 1), (1, 1))
        """
        CurrentState.__init__(self, player)
        self._p1 = p1
        self._p2 = p2

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves for the current player.
        >>> c = ChopsticksState('p1', (1, 1), (1, 1))
        >>> c.get_possible_moves()
        ['ll', 'lr', 'rl', 'rr']
        >>> c2 = ChopsticksState('p1', (0, 0), (0, 0))
        >>> c2.get_possible_moves()
        []
        """
        player = self.get_current_player_name()
        result = []
        if player == 'p1':
            player_hand = self._p1
            oppo_hand = self._p2
        else:
            player_hand = self._p2
            oppo_hand = self._p1
        if player_hand[0] != 0 and oppo_hand[0] != 0:
            result.append('ll')
        if player_hand[0] != 0 and oppo_hand[1] != 0:
            result.append('lr')
        if player_hand[1] != 0 and oppo_hand[0] != 0:
            result.append('rl')
        if player_hand[1] != 0 and oppo_hand[1] != 0:
            result.append('rr')
        return result

    def make_move(self, move_to_make: str) -> 'ChopsticksState':
        """
        Add the elements of move_to_make to the same index of another
        player's hand.
        >>> c = ChopsticksState('p1', (1, 1), (1, 1))
        >>> print(c.make_move('ll'))
        Player 1: 1 - 1; Player 2: 2 - 1
        """
        result_oppo = ''
        player = self.get_current_player_name()
        if player == 'p1':
            player_hand = self._p1
            oppo_hand = self._p2
        else:
            player_hand = self._p2
            oppo_hand = self._p1
        if move_to_make == 'll':
            result_oppo = (oppo_hand[0] + player_hand[0], oppo_hand[1])
        elif move_to_make == 'lr':
            result_oppo = (oppo_hand[0], oppo_hand[1] + player_hand[0])
        elif move_to_make == 'rl':
            result_oppo = (oppo_hand[0] + player_hand[1], oppo_hand[1])
        elif move_to_make == 'rr':
            result_oppo = (oppo_hand[0], oppo_hand[1] + player_hand[1])

        answer_oppo = (result_oppo[0] % 5, result_oppo[1] % 5)
        if player == 'p1':
            new_state = ChopsticksState('p2', self._p1, answer_oppo)
        else:
            new_state = ChopsticksState('p1', answer_oppo, self._p2)
        return new_state

    def is_over(self) -> bool:
        """
        Return whether the Chopsticks game self is over.
        >>> c = ChopsticksState('p1', (0, 0), (1, 1))
        >>> c.is_over()
        True
        """
        return self._p1 == (0, 0) or self._p2 == (0, 0)

    def __str__(self) -> str:
        """
        Return a string representation of self.
        >>> c = ChopsticksState('p1', (1, 1), (1, 1))
        >>> print(c)
        Player 1: 1 - 1; Player 2: 1 - 1
        """
        return ("Player 1: {} - {}; Player 2: {} - {}".format(self._p1[0],
                                                              self._p1[1],
                                                              self._p2[0],
                                                              self._p2[1]))

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
