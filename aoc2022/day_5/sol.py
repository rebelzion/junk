from typing import Optional
import sys
import re

# CONFIG
LEVEL = 2


def read_input(fn: Optional[str] = sys.stdin) -> str:
  # Read the input from the given file or stdin
  lines = []
  ifn = open(fn) if isinstance(fn, str) else fn
  lines = ifn.readlines()

  # Return the input as a string
  return ''.join(lines)

def solve(input_str: str, flip) -> str:
  # Split the input string into lines
  lines = input_str.split('\n')
  # print(f"{lines=}")

  # Parse the input to create a list of stacks, where each stack is represented as a list of crates
  stacks = {}
  for idx_line, line in enumerate(lines):
    if '[' not in line:
        break

    i = 0
    stack_id = 0
    spaces = 0
    while i < len(line):
        c = line[i]
        if c == '[':
            if spaces > 0:
                if spaces == 1:
                    stack_id += 1
                elif spaces % 2 == 0:
                    stack_id += (spaces-1) // 3
                else:
                    spaces -= 2
                    num_stacks = spaces // 3
                    stack_id += num_stacks + 1
                spaces = 0
            if stack_id not in stacks:
                stacks[stack_id] = []
            stacks[stack_id].append(line[i+1])
            i += 3
        elif c == ' ':
            spaces += 1
            i += 1

  #print(f"{stacks=}")
  for i in range(idx_line+2, len(lines)):
      line = lines[i].strip()
      if not line:
          continue
      matches = r = re.match(r'move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)', line)
      how_many = int(matches[1])
      fr = int(matches[2])
      to = int(matches[3])
      fr -= 1
      to -= 1

      #print(f"move {how_many} from {fr} to {to}")

      if flip:
        what = list(reversed(stacks[fr][:how_many]))
      else:
        what = stacks[fr][:how_many]

      stacks[to] = what + stacks[to]
      stacks[fr] = stacks[fr][how_many:]

      #print(f"stacks=")
      #for i in range(len(stacks)):
      #    print(f"\t{stacks[i]}")

  message = ''.join([stacks[i][0] for i in range(len(stacks))])

  return message


def write_output(result: str) -> str:
  # Return the result as a string
  return result

if __name__ == '__main__':
  # Read the input
  inp = read_input()

  # Solve the problem
  res = solve(inp, flip = (LEVEL == 1))

  # Print the result
  print(write_output(res))

