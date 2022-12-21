import sys
from collections import deque

def parse_input(lines):
    # Convert the input lines into a 2D list of characters
    heightmap = [list(line) for line in lines]

    # Find the start and end positions
    for y, row in enumerate(heightmap):
        for x, c in enumerate(row):
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)

    return (heightmap, start, end)

def solve(input, level=1):

    heightmap, start, end = input
    heightmap[start[1]][start[0]] = 'a'
    heightmap[end[1]][end[0]] = 'z'

    # Find all of the starting positions at elevation a
    starts = [(*start, 0)] if level == 1 else [(x, y, 0) for y in range(len(heightmap)) for x in range(len(heightmap[0])) if heightmap[y][x] == 'a']

    # Set up the queue and visited set
    queue = deque(starts)
    visited = set(starts)
    solution = [['.' for j in range(len(heightmap[0]))] for i in range(len(heightmap))]

    # Keep searching until we find the end position or the queue is empty
    min_steps = float('inf')
    while queue:
        # Dequeue a position from the queue
        x, y, steps = queue.popleft()

        # Check if we've reached the end position
        if (x, y) == end:
            min_steps = min(min_steps, steps)
            #return steps, solution
        else:
            # Add the valid neighbors of this position to the queue and mark them as visited
            for dx, dy, direction in [(1, 0, '>'), (-1, 0, '<'), (0, 1, 'v'), (0, -1,'^')]:
                # Calculate the new position
                new_x, new_y = x + dx, y + dy

                # Check if the new position is within the grid and has an elevation difference of at most 1
                if 0 <= new_x < len(heightmap[0]) and 0 <= new_y < len(heightmap) and ord(heightmap[new_y][new_x]) - ord(heightmap[y][x]) <= 1 and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y, steps+1))  # Increment the step counter when adding the position to the queue
                    solution[y][x] = direction
                    visited.add((new_x, new_y))

    # If we reach this point, it means that we were unable to find the end position
    return min_steps, solution


test_input = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]

inp = []
for line in sys.stdin:
    inp.append(line.strip())

input = parse_input(inp)
steps, solution = solve(input, level=2)
print(f'{steps=}')
print()

print('Solution:')
for row in solution:
    print(''.join(row))
