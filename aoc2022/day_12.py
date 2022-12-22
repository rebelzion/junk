import sys
from collections import deque

def parse_input(lines):
    # Convert the input lines into a 2D list of characters
    heightmap = [list(line) for line in lines]

    # Find the start and end positions
    for i, row in enumerate(heightmap):
        for j, c in enumerate(row):
            if c == 'S':
                start = (i, j)
            elif c == 'E':
                end = (i, j)

    return (heightmap, start, end)

def solve(input, level=1):

    heightmap, start, end = input
    heightmap[start[0]][start[1]] = 'a'
    heightmap[end[0]][end[1]] = 'z'

    # Find all of the starting positions at elevation a
    starts = [(*start, 0)] if level == 1 else [(i, j, 0) for i in range(len(heightmap)) for j in range(len(heightmap[0])) if heightmap[i][j] == 'a']

    # Set up the queue and visited set
    queue = deque(starts)
    visited = set((i,j) for (i,j, _) in starts)
    solution = [['.' for j in range(len(heightmap[0]))] for i in range(len(heightmap))]
    stepsmap = [[0 for j in range(len(heightmap[0]))] for i in range(len(heightmap))]
    for i,j,steps in starts:
        stepsmap[i][j] = steps

    # Keep searching until we find the end position or the queue is empty
    min_steps = float('inf')
    while queue:
        # Dequeue a position from the queue
        i, j, steps = queue.popleft()

        # Check if we've reached the end position
        if (i, j) == end:
            min_steps = min(min_steps, steps)
            #return steps, solution
        else:
            # Add the valid neighbors of this position to the queue and mark them as visited
            for di, dj, direction in [(1, 0, 'v'), (-1, 0, '^'), (0, 1, '>'), (0, -1,'<')]:
                # Calculate the new position
                new_i, new_j = i + di, j + dj

                # Check if the new position is within the grid and has an elevation difference of at most 1
                if 0 <= new_i < len(heightmap) and 0 <= new_j < len(heightmap[0]) and ord(heightmap[new_i][new_j]) - ord(heightmap[i][j]) <= 1 and (new_i, new_j) not in visited:
                    queue.append((new_i, new_j, steps+1))  # Increment the step counter when adding the position to the queue
                    solution[i][j] = direction
                    stepsmap[new_i][new_j] = steps+1
                    visited.add((new_i, new_j))

    # If we reach this point, it means that we were unable to find the end position
    return min_steps, solution, stepsmap


def read_input(fp = None):

    if isinstance(fp, str):
        with open(fp, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
    else:
        lines = [line.strip() for line in sys.stdin]
    return lines

if __name__ == '__main__':

    test_input = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]

    input = parse_input(read_input())
    steps, solution, _ = solve(input, level=1)
    print(f'{steps=}')
    print()

    print('Solution:')
    for row in solution:
        print(''.join(row))
