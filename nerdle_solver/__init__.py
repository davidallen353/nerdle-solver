"""Tools to solve Nerdle puzzles."""
import imp
import itertools
from logging import getLogger
from tqdm import tqdm

from copy import deepcopy

logger=getLogger(__name__)

DIGITS= ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ]
OPERATORS = ["+", "-", "*", "/", "=",]
GUESS_LENGTH = 8

DEFAULT_KNOWN_BAD_CHAR = {
    0: deepcopy(OPERATORS), 
    1: ["=", ], 
    2: ["=", ], 
    3: ["="], 
    4: ["", ], 
    5: ["+", "-", "*", "/"],
    6: ["+", "-", "*", "/"], 
    7: deepcopy(OPERATORS),}

def check_valid_equation(equation_str: str) -> bool:
    """Check if the equation is valid.

    Args:
        equation_str: The equation to check.

    Returns:
        True if the equation is valid, False otherwise.
    """
    if equation_str.count("=") != 1:
        return False

    left_side, right_side = equation_str.split("=")
    left_side = left_side.strip()
    right_side = right_side.strip()

    if left_side == "" or right_side == "":
        return False

    for _i in range(len(left_side)-1):
        if left_side[_i] in OPERATORS and left_side[_i+1] in OPERATORS:
            return False

    if right_side[0] == "0":
        return False
    if left_side[0] == "0":
        return False

    try:
        return eval(left_side) == eval(right_side)
    except SyntaxError:
        logger.debug("Syntax error in equation: " + equation_str)
        return False
    except ZeroDivisionError:
        logger.debug("Division by zero in equation: " + equation_str)
        return False

def build_character_list(bad_chars) -> list:
    """Build a list of all possible characters.

    Args:
        bad_digits: A list of digits to exclude.
        bad_operators: A list of operators to exclude.

    Returns:
        A list of all possible characters.
    """
    character_list = []
    for digit in DIGITS:
        if digit not in bad_chars:
            character_list.append(digit)

    for operator in OPERATORS:
        if operator not in bad_chars:
            character_list.append(operator)

    return character_list

def generate_guesses(character_list:list, known_char: list, good_char: list, known_bad_char: dict) -> list:
    """Generate all possible guesses.

    Args:
        character_list: A list of all possible characters.

    Returns:
        A list of all possible guesses.
    """
    guesses = []
    if len(known_char) != GUESS_LENGTH:
        raise ValueError("known_char must be of length " + str(GUESS_LENGTH))
    
    _char_list = known_char
    print("a", _char_list)
    for i in range(GUESS_LENGTH):
        if _char_list[i] == "":
            _char_list[i] = [_char for _char in character_list if _char not in known_bad_char[i]]

    print("b", _char_list)
    for _list in tqdm(list(itertools.product(*_char_list)), desc="Generating guesses"):
        guess = "".join(_list)

        if check_valid_equation(guess):
            if all([_char in guess for _char in good_char]):
                guesses.append(guess)

    return guesses

def make_recommendation(guesses: list, good_chars: list,) -> str:
    """Recommend a guess.

    Attempts to find the most new information

    Args:
        guesses: A list of all possible guesses.
        good_chars: A list of good characters.

    Returns:
        A recommended guess.
    """
    guess_scores = []

    # Bad digits should be filtered out
    _unkown_chars = [_char for _char in DIGITS + OPERATORS if _char not in good_chars]

    for guess in guesses:
        _score = 0
        for _char in _unkown_chars:
            if _char in guess:
                _score += 1
            _score += guess.count(_char)
        guess_scores.append(_score)

    return guesses[guess_scores.index(max(guess_scores))]