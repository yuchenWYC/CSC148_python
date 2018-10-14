"""Helper functions for a1"""


def get_start_number() -> int:
    """
    Return a non-negative integer the user chooses to start the game Substract
    Square.
     """
    candidate = input("Please enter a non-negative integer:")
    while not candidate.isdigit():
        candidate = input("Please enter a non-negative integer:")
    return int(candidate)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a1_pyta.txt')
