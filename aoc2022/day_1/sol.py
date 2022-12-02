import heapq

max_sum = 0
cur_sum = 0
sums = []
for line in open('input.txt'):
    line = line.strip()
    if not line:
        max_sum = max(cur_sum, max_sum)
        sums.append(cur_sum)
        cur_sum = 0
    else:
        cur_sum += int(line)

sums.append(cur_sum)

top_three = heapq.nlargest(3, sums)
print(sum(top_three))
