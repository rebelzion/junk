from time import perf_counter
from contextlib import contextmanager
import matplotlib.pyplot as plt
from typing import Union, Tuple, Optional, List, Iterable, Callable
import sys


def merge_segments(segments: Iterable[Tuple[int, int]]) -> Iterable[Tuple[int, int]]:
    """
    O(N * log(N)) solution to merge a list of segments if they overlap.
    Overlap for (l1, r1), (l2, r2) means r1 >= l2.
    """
    # sort the segments by left_x value
    segments.sort(key=lambda x: x[0])

    # initialize the list of merged segments
    merged = []

    # iterate through the sorted segments
    for segment in segments:
        # if the current segment overlaps with the previous segment, merge them
        if merged and segment[0] <= merged[-1][1]:
            merged[-1] = (min(merged[-1][0], segment[0]),
                          max(merged[-1][1], segment[1]))
        # if the current segment does not overlap with the previous segment, append it to the list of merged segments
        else:
            merged.append(segment)

    return merged


def get_distance(x1, y1, x2, y2, norm=1):
    if norm == 1:
        return abs(x1 - x2) + abs(y1 - y2)
    else:
        raise ValueError(f"Implement {norm=}!")


@contextmanager
def timeit(return_val=False) -> None:
    tic = perf_counter()
    if return_val:
        yield lambda: perf_counter() - tic
    else:
        yield
        print(f"Execution time: {(perf_counter() - tic):.4f} sec")


def read_input(fn: Optional[str] = None, ignore_empty_lines: bool = False) -> List[str]:

    ifn = open(fn) if fn else sys.stdin
    return list(filter(lambda x: ignore_empty_lines and x or not ignore_empty_lines, [line.rstrip() for line in ifn.readlines()]))


def plot(points, size: Union[int, Tuple[int, int]] = (10, 10), marker='o', **kwargs):

    if size:
        plt.figure(figsize=(size, size) if isinstance(size, int) else size)
    plt.axis("off")

    plt.plot(*zip(*points), marker=marker, **kwargs)
    plt.show()


def get_path(solution, start, end, max_steps=None):
    """
    Computes a path given number of steps in `solution`.
    """
    path = []
    i, j = end
    step = 0
    while (i, j) != start:
        path.append((i, j))
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if 0 <= i+di < len(solution) and 0 <= j+dj < len(solution[0]):
                if solution[i+di][j+dj] == solution[i][j]-1:
                    i, j = i+di, j+dj
                    break
        step += 1
        if max_steps is not None and step > max_steps:
            break
    path.append((i, j))
    return path


def get_extreme(lst: Iterable[Iterable[int]], axis: int, func: Callable[..., int]) -> List[int]:

    if axis == 1:
        res = [func(el) for el in lst]
    elif axis == 0:
        ncols = len(lst[0])
        res = [None for i in range(ncols)]
        for el in lst:
            for i in range(ncols):
                res[i] = el[i] if res[i] is None else func(res[i], el[i])
    return res
