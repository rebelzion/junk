# TODO @vronin: simplify the code
import sys
from itertools import accumulate
import numpy as np

def count_visible_trees(grid):
    grid = np.array(grid)
    total_count = 0
    max_p = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            tree = grid[row][col]
            count = 0
            ps = [1 for _ in range(4)]
            # Check if this tree is the maximum when viewed from the left
            if col == 0 or tree > max(grid[row,:col] if col > 0 else []):
                count = 1
            _p = col
            for ii in range(col-1, -1, -1):
                if grid[row][ii] >= tree:
                    _p = col - ii
                    break
            ps[0] = _p
            # Check if this tree is the maximum when viewed from the right
            if col == len(grid[0]) - 1 or tree > max(grid[row,col+1:]):
                count = 1
            _p = len(grid[0]) - col - 1
            for ii in range(col+1, len(grid[0])):
                if grid[row][ii] >= tree:
                    _p = ii - col
                    break
            ps[1] = _p
            # Check if this tree is the maximum when viewed from the top
            if row == 0 or tree > max(grid[:row,col] if row > 0 else []):
                count = 1
            _p = row
            for ii in range(row-1, -1, -1):
                if grid[ii][col] >= tree:
                    _p = row - ii
                    break
            ps[2] = _p
            # Check if this tree is the maximum when viewed from the bottom
            if row == len(grid) - 1 or tree > max(grid[row+1:,col]):
                count = 1
            _p = len(grid)-row-1
            for ii in range(row+1, len(grid)):
                if grid[ii][col] >= tree:
                    _p = ii - row
                    break
            ps[3] = _p

            total_count += count
            if count > 0 and row > 0 and col > 0 and row < len(grid)-1 and col < len(grid[0])-1:
                max_p = max(max_p, list(accumulate(ps, lambda x,y: x*y))[-1])


    return total_count, max_p



grid = []
for line in sys.stdin:
    row = list(map(int, [*line.strip()]))
    grid.append(row)

print(f"rows={len(grid)}, cols={len(grid[0])}")

res = count_visible_trees(grid)
print(res)
