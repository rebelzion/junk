from typing import Optional, Tuple
import math
import sys
import logging
import functools

logging.basicConfig(level=logging.DEBUG)


def lcm2(a, b):
    return abs(a*b) // math.gcd(a, b)


def lcm(numbers):
    if numbers:
        return functools.reduce(lambda x, y: lcm2(x, y), numbers)
    else:
        return 1


def read_input(fn: Optional[str] = sys.stdin) -> str:
    lines = []
    ifn = open(fn) if isinstance(fn, str) else fn
    lines = ifn.readlines()
    return ''.join(lines)

def solve(input_str: str) -> str:
    # Parse the input
    lines = input_str.strip().split("\n")
    c, d = map(int, lines[0].split())
    # transcript = [w for w in lines[1].split() if w.isalpha()]
    transcript = lines[1].split()

    logging.debug(f"{transcript=}")

    i = c
    merry = []
    christmas = []
    for w in transcript:
        if w.isalpha():
            if w == "Merry":
                merry.append(i)
                i += 1
            elif w == "Christmas":
                christmas.append(i)
                i += 1
            elif w == "MerryChristmas":
                merry.append(i)
                christmas.append(i)
                i += 1
        else:
            i = int(w)+1


    print(f"{merry=}")
    print(f"{christmas=}")


    # Find the frequency at which "Merry" and "Christmas" are sung
    a = lcm(merry)
    b = lcm(christmas)

    print(f"lcm a = ", a, "lcm b = ", b)

    print("lcm (a,b) = ", lcm(numbers=[a,b]))


    if len(merry) > 1:
        a = merry[1] - merry[0]

    if len(christmas) > 1:
        b = christmas[1] - christmas[0]

    print("a = ", a, "b = ", b)

    # # Find the frequency at which "MerryChristmas" is sung
    # b = lcm(a, both)

    # # Find the smallest possible values for the frequencies at which "Merry" and "Christmas" are sung
    # a //= math.gcd(a, b)
    # b //= math.gcd(a, b)

    return a,b



def write_output(result) -> str:
   print(f"{result[0]} {result[1]}")


if __name__ == '__main__':
    inp = read_input()
    res = solve(inp)
    write_output(res)
