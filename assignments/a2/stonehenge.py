"""
An implementation of game stonehenge.
"""
from typing import Any, List, Union
from copy import deepcopy
from game import Game
from game_state import GameState


class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.
    """

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this StonehengeGame, using p1_starts to find who the first
        player is.

        :param p1_starts: A boolean representing whether Player 1 is the first
                                 to make a move.
        """
        size = int(input("Enter the size length of the board: "))
        lay_line_markers = [["@"] * (size + 1)] * 3
        cells = self.cell_list(size)
        self.current_state = StonehengeState(p1_starts, size, cells,
                                             lay_line_markers)

    def cell_list(self, size: int) -> List[List[str]]:
        """
        Return a cell list generated according to size. The cell list is used
        when initizing a new StonehengeGame.
        """
        alpha_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                      'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                      'W', 'X', 'Y', 'Z']
        start, end = 0, 1
        result = []
        for i in range(2, size + 2):
            line = alpha_list[start: end + 1]
            result.append(line)
            start = end + 1
            end = start + i
        last_line = alpha_list[start: start + size]
        result.append(last_line)
        return result

    def get_instructions(self) -> str:
        """
        Return the instructions for this StonehengeGame.
        """
        instructions = "Players take turns claiming cells. When a player " + \
            "captures at least half of the cells in a leyline, then the " + \
            "player captures that ley-line. The first player to capture " + \
            "at least half of the ley-lines is the winner. A ley-line " + \
            "once claimed, cannot be taken by the other player."
        return instructions

    def is_over(self, state: 'StonehengeState') -> bool:
        """
        Return whether or not this StonehengeGame is over at this
        StonehengeState.
        """
        return state.get_possible_moves() == []

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the StonehengeGame.

        Precondition: player is 'p1' or 'p2'.
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If string is not a move,
        return some invalid move.
        :param string: Is a move when it is a capital letter("A", "B", etc)
        """
        return string if self.current_state.is_valid_move(string) else '-1'

    def __eq__(self, other: Any) -> bool:
        """
        Return True iff self is equivalent to other.
        """
        return (type(self) == type(other)
                and self.current_state == other.current_state)

    def __str__(self) -> str:
        """
        Return a string representation of self.
        """
        r = "Game Stonehenge with side length {}"
        return r.format(self.current_state.size)


class StonehengeState(GameState):
    """
    The state of a StonehengeGame at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, size: int, cells: List[List[str]],
                 ley_line_markers: List[List[str]]) -> None:
        """
        Initialize this Stonehengestate and set the current player based on
        is_p1_turn.
        Extends GameState.__init__
        """
        GameState.__init__(self, is_p1_turn)
        self.size = size
        self.cells = cells
        self.ley_line_markers = ley_line_markers

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the
        StonehengeGame.
        """
        cells_n_dashes = self.insert_dash(self.cells)
        slashes = self.generate_slash()
        board = self.generate_board(cells_n_dashes, slashes)
        self.add_markers(board)
        self.add_space(board)
        sum_board = '\n'.join(board)
        return sum_board

    def insert_dash(self, cells_list: List[List[str]]) -> List[str]:
        """
        Insert ' - 'in the middle of every two cells in each line of cells.
        """
        return [''.join(add_between(line, ' - ')) for line in cells_list]

    def generate_slash(self) -> List[str]:
        """
        Generate lines of '/' and '\' to be inserted betweeen every two lines of
        cells_n_dashes to connect each cell as well as to connect cells and
        ley-line markers.
        """
        first_line = '/   /'
        last_line = '   '.join('\\' * self.size)
        last_line2 = '\\ / ' * self.size + '\\'
        i = 0
        result = []
        while i != len(self.cells) - 2:
            length = min(len(self.cells[i]), len(self.cells[i]) + 1)
            line = '/ \\ ' * length + '/'
            result.append(line)
            i += 1
        result.insert(0, first_line)
        result.append(last_line2)
        result.append(last_line)
        return result

    def generate_board(self, cells_n_dashes: List[str], slashes: List[str]) \
            -> List[str]:
        """
        Insert the slashes into lines of cells_n_dashes to make connections
        between cells and ley-line markers.
        """
        return add_between(slashes, cells_n_dashes)

    def add_markers(self, pre_board: List[str]) -> None:
        """
        Insert ley-line markers into pre_board.
        """
        # from top to bottom
        first_line = '{}   {}'.format(self.ley_line_markers[2][0],
                                      self.ley_line_markers[2][1])
        for i in range(len(pre_board)):
            if i % 2 == 1 and i < len(pre_board) - 4:
                pre_board[i] = ' ' * abs(len(pre_board) - 4 - i) + \
                 '{} - '.format(self.ley_line_markers[0][int((i - 1) / 2)]) + \
                 pre_board[i] + \
                 '   {}'.format(self.ley_line_markers[2][int((i + 3) / 2)])
            elif i % 2 == 1 and i == len(pre_board) - 4:
                pre_board[i] = \
                 '{} - '.format(self.ley_line_markers[0][int((i - 1) / 2)]) + \
                 pre_board[i]
            elif i == len(pre_board) - 2:
                pre_board[i] = ' ' * abs(len(pre_board) - 4 - i) + \
                 '{} - '.format(self.ley_line_markers[0][int((i - 1) / 2)]) + \
                 pre_board[i] + \
                 '   {}'.format(self.ley_line_markers[1][-1])

        pre_last_line = '   '.join(self.ley_line_markers[1][:-1])
        last_line = '        ' + pre_last_line
        pre_board.insert(0, first_line)
        pre_board.append(last_line)

    def add_space(self, board: List[str]) -> None:
        """
        Add space to the slashes lines to make the board more readible when
        printed.
        """
        for i in range(len(board)):
            if i % 2 == 1:
                board[i] = '    ' + ' ' * abs(len(board) - 5 - i) + \
                            board[i]
        board[0] = '     ' + ' ' * abs(len(board) - 6) + board[0]

    def get_possible_moves(self) -> List[str]:
        """
        Return all possible moves that can be applied to this state.
        """
        count1, count2 = 0, 0
        for group in self.ley_line_markers:
            for marker in group:
                if marker == '1':
                    count1 += 1
                elif marker == '2':
                    count2 += 1
        if (count1 >= len(self.ley_line_markers[0] * 3) / 2 or
                count2 >= len(self.ley_line_markers[0] * 3) / 2):
            return []
        result = []
        for line in self.cells:
            for cell in line:
                if cell != '1' and cell != '2':
                    result.append(cell)
        return result

    def markers_after_claimed(self, markers: List[List[str]],
                              cells: List[List[str]],
                              indexl: int, indexm: int) -> List[List[str]]:
        """
        Return markers after claiming by the player of the current turn.
        The player can claim a marker iff they had newly captured at least
        half of the cells in a ley-line.
        """
        indexm_inverse = indexm - len(cells[indexl])
        # horizontal:
        group1 = markers[0][:]
        if group1[indexl] == '@':
            self.claim_marker(cells[indexl], group1, indexl)

        # diagonal-right:
        group2 = markers[1][:]
        if indexl + 1 != len(cells):
            if group2[indexm_inverse] == '@':
                ley_line = self.dr_leyline_v1(cells, indexm, indexm_inverse)
                self.claim_marker(ley_line, group2, indexm_inverse)
        else:
            if group2[indexm_inverse - 1] == '@':
                ley_line = self.dr_leyline_v2(cells, indexm_inverse)
                self.claim_marker(ley_line, group2, indexm_inverse - 1)

        # diagonal-left:
        group3 = markers[2][:]
        if indexl + 1 != len(cells):
            if group3[indexm] == '@':
                ley_line = self.dl_leyline_v1(cells, indexm)
                self.claim_marker(ley_line, group3, indexm)
        else:
            if group3[indexm + 1] == '@':
                ley_line = self.dl_leyline_v2(cells, indexm)
                self.claim_marker(ley_line, group3, indexm + 1)

        return [group1, group2, group3]

    def dr_leyline_v1(self, cells: List[List[str]], indexm: int,
                      indexm_inverse: int) -> List[str]:
        """
        Return a diagonal-right ley-line in the condition that move made
        is NOT in the last line of cells.
        """
        ley_line = []
        for layer in cells[:-1]:
            if -1 * indexm_inverse <= len(layer):
                ley_line.append(layer[indexm_inverse])
        if indexm <= len(cells[-1]) - 2:
            ley_line.append(cells[-1][indexm_inverse + 1])
        return ley_line

    def dr_leyline_v2(self, cells: List[List[str]],
                      indexm_inverse: int) -> List[str]:
        """
        Return a diagonal-right ley-line in the condition that move made
        is in the last line of cells.
        """
        ley_line = []
        for layer in cells[:-1]:
            if -1 * (indexm_inverse - 1) <= len(layer):
                ley_line.append(layer[indexm_inverse - 1])
        ley_line.append(cells[-1][indexm_inverse])
        return ley_line

    def dl_leyline_v1(self, cells: List[List[str]], indexm: int) -> List[str]:
        """
        Return a diagonal-left ley-line in the condition that move made
        is NOT in the last line of cells.
        """
        ley_line = []
        for layer in cells[:-1]:
            if indexm <= len(layer) - 1:
                ley_line.append(layer[indexm])
        if 0 <= indexm - 1 <= len(cells[-1]):
            ley_line.append(cells[-1][indexm - 1])
        return ley_line

    def dl_leyline_v2(self, cells: List[List[str]], indexm: int) -> List[str]:
        """
        Return a diagonal-left ley-line in the condition that move made
        is in the last line of cells.
        """
        ley_line = []
        for layer in cells[:-1]:
            if indexm + 1 <= len(layer) - 1:
                ley_line.append(layer[indexm + 1])
        ley_line.append(cells[-1][indexm])
        return ley_line

    def make_move(self, move: str) -> 'StonehengeState':
        """
        Return the StonehengeState that results from applying move to this
        StonehengeState.
        """
        if not self.is_valid_move(move):
            return self
        cells = deepcopy(self.cells)
        markers = deepcopy(self.ley_line_markers)
        index_move = [(i, el.index(move)) for i, el
                      in enumerate(cells) if move in el]
        indexl = index_move[0][0]
        indexm = index_move[0][1]
        cells[indexl][indexm] = self.display_player()
        new_markers = self.markers_after_claimed(markers, cells, indexl,
                                                 indexm)
        return StonehengeState(self.take_turn(), self.size,
                               cells, new_markers)

    def claim_marker(self, ley_line: List[str], marker_list: List[str],
                     index: int) -> None:
        """
        Let the current player claim the marker in marker_list at index
        iff the player newly captured at least half of the cells in ley_line.
        """
        player = self.display_player()
        count = ley_line.count(player)
        if count >= len(ley_line) / 2:
            marker_list[index] = player

    def display_player(self) -> str:
        """
        Return '1' if it is player 1's turn to play, return '2' if it is player
        2's turn to play.
        """
        return '1' if self.p1_turn is True else '2'

    def take_turn(self) -> bool:
        """
        Return True iff this is player 2's turn.
        """
        return False if self.p1_turn is True else True

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        r = "P1's turn: {} - Board size: {} - Cells: {} - Ley-line markers: {}"
        return r.format(self.p1_turn, self.size, self.cells,
                        self.ley_line_markers)

    def max_after_claim(self) -> int:
        """
        Return the most number of ley-lines already claimed by the current
        player after one of the possible moves is applied.
        """
        result = []
        for move in self.get_possible_moves():
            sum_ley_line = sum(self.make_move(move).ley_line_markers, [])
            number_claimed = sum([1 if marker == self.display_player() else 0
                                  for marker in sum_ley_line])
            result.append(number_claimed)
        return max(result)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee in at most two states ahead.
        """
        if self.get_possible_moves() == []:
            return self.LOSE
        else:
            number_ley_line = len(self.ley_line_markers[0]) * 3
            if self.max_after_claim() >= number_ley_line / 2:
                return self.WIN
            elif all([self.make_move(move).max_after_claim() >= number_ley_line
                      / 2 for move in self.get_possible_moves()]):
                return self.LOSE
            return self.DRAW


def add_between(list_to_add: list, const: Union[list, str]) -> list:
    """
    Add const as a new list element between every two elements in
    list_to_add.
    If const is a list and length of list_to_add is greater than one,
    then the length of const must be 1 less than the length of list_to_add.
    >>> add_between(['a', 'b', 'c'], '1')
    ['a', '1', 'b', '1', 'c']
    >>> add_between(['single'], 'whatever')
    ['single']
    >>> add_between(['a', 'b', 'c'], ['1', '2'])
    ['a', '1', 'b', '2', 'c']
    """
    result = []
    if len(list_to_add) <= 1:
        return list_to_add
    if not isinstance(const, list):
        const = [const] * (len(list_to_add) - 1)
    for i in range(len(const)):
        result.append(list_to_add[i])
        result.append(const[i])
    result.append(list_to_add[-1])
    return result


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
