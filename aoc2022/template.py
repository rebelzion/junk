from typing import Optional
import sys
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


def read_input(fn: Optional[str] = None):

    ifn = open(fn) if fn else sys.stdin

    return ''.join(ifn.readlines())


def parse_input(input_lines_str: str):
    """
    Parse the `input_lines_str` according to the problme statement.
    """
    pass


def solve(**kwargs) -> str:
    """
    Solve the problem using `kwargs` as input and return the result
    in string format.
    """
    pass


def generate_tests():
    """
    Write some tests
    """
    tests = []
    return tests

@pytest.mark.parametrize("test_input,expected", [(inp, exp) for inp, exp in generate_tests()])
def test_solve(test_input, expected):
    assert (solve(test_input) == expected)


if __name__ == '__main__':
    fn = sys.argv[1] if len(sys.argv) > 1 else None
    logging.debug(f"Using {fn} as input file")

    input_str = read_input(fn=fn)
    logging.debug(input_str)
