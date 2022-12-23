import sys

# Coordinates of the head and tail
head = (0, 0)
tail = (0, 0)

# The movement directions
directions = {"U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0)}

# Parse the input
for line in sys.stdin:
  # Read the next movement
  line = line.strip()
  direction, steps = line.split()
  steps = int(steps)

  # Update the head position
  head = (head[0] + directions[direction][0] * steps, head[1] + directions[direction][1] * steps)

  # Update the tail position based on the rules described in the problem statement
  if head == tail:
    # If the head and the tail overlap, move the tail one step in the direction of the head
    tail = (tail[0] + directions[direction][0], tail[1] + directions[direction][1])
  elif abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
    # If the head is more than one step away from the tail,
    # move the tail one step in the direction of the head
    tail = (tail[0] + (head[0] - tail[0]) // abs(head[0] - tail[0]), tail[1] + (head[1] - tail[1]) // abs(head[1] - tail[1]))
  elif (head[0] == tail[0] or head[1] == tail[1]) and direction in {"U", "D", "L", "R"}:
    # If the head and tail are in the same column or row, but not overlapping,
    # and the head moves horizontally or vertically,
    # move the tail one step in the direction of the head
    tail = (tail[0] + directions[direction][0], tail[1] + directions[direction][1])

# Print the final position of the tail
print(tail[0], tail[1])
