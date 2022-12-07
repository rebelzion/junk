"""
Funny problem :) Read the statement first and try solving it yourself before looking at the solution.

Problem Statement:
---
Given a string of digits spelled out as words and possibly scrambled,
return a string containing the numerical values of the digits in increasingly sorted order.

Examples:
---
"otw" -> "2"
"onexisone" -> "166"

To run the tests, run in terminal:
pytest scrambled.py:test_get_scrambled_digits

"""


from random import seed, randint, shuffle
import pytest
from typing import Tuple

# NOTE: we can comment this out for testing
#seed(0)

def gen_test(num_digits: int) -> Tuple[str, str]:

    d2w = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }

    digits = [randint(0,9) for _ in range(num_digits)]
    word_digits = list(map(lambda x: d2w[x], digits))

    lst = [c for d in word_digits for c in d]
    shuffle(lst)

    s = ''.join(lst)
    expected = ''.join(map(str, sorted(digits)))

    return s, expected


def get_scrambled_digits(inp: str) -> str:
    # Helpful mapping to construct the final result
    w2d= {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    # This the whole spiel of the problem!
    stages = [
        {
            "z": "zero",
            "w": "two",
            "x": "six",
            "g": "eight"
        },
        {
            "t": "three",
            "s": "seven",
        },
        {
            "r": "four",
        },
        {
            "f": "five",
            "v": "five",
        },
        {
            "o": "one",
        },
        {
            "n": "nine",
        }
    ]

    # construct letter frequency of the input
    l2f = {}
    for c in inp:
        if c not in l2f:
            l2f[c] = 0
        l2f[c] += 1

    # construct the solution in stages by trying out the different digits.
    res = ""
    for stage in stages:
        for c, digit in stage.items():
            while c in l2f and l2f[c] > 0: # needed in case we have duplicates of a digit
                for digit_chr in digit:
                    l2f[digit_chr] -= 1
                res += w2d[digit]

    return "".join(sorted(res))


@pytest.mark.parametrize("inp,exp", [gen_test(3), ("", ""), ("otw", "2"), ("nifourne", "49"), gen_test(10)])
def test_get_scrambled_digits(inp, exp):
    assert get_scrambled_digits(inp) == exp

