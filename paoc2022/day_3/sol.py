INP = 'input.txt'
INP = None

lines = [line.strip() for line in open('input.txt')] if INP else []

n = int(lines[0]) if INP else int(input())

transitions = {}

for i in range(1, n+1):
  curr_transition = lines[i].split() if INP else input().split()
  out_node = int(curr_transition[0])
  c = curr_transition[2]
  target_node = int(curr_transition[4])

  if out_node not in transitions:
    transitions[out_node] = {}

  transitions[out_node][c] = target_node

I = lines[-1] if INP else input()

curr_node = 0
for c in I:
  curr_node = transitions[curr_node][c]

print(curr_node)

