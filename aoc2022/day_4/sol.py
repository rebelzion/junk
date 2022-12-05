# Co-created with ChatGPT

# CONFIG
LEVEL = 2


def parse_input(input_str):
    # split the input string into a list of strings, each representing a range
    ranges = input_str.strip().splitlines()

    # convert each string into a tuple of integers (start, end)
    ranges = [tuple(map(int, r.split('-'))) for rs in ranges for r in rs.split(',')]

    return ranges

def is_fully_contained(range1, range2, level=1):
    # check if the start and end of range1 are both less than or equal to the start and end of range2, respectively
    if level == 1:
        return (range1[0] <= range2[0] and range1[1] >= range2[1]) or (range2[0] <= range1[0] and range2[1] >= range1[1])
    else:
        if range2[0] <= range1[0]:
            range1, range2 = range2, range1
        return range1[1] >= range2[0]


def num_fully_contained_pairs(ranges, level=1):
    # initialize the counter for the number of fully contained pairs
    num_pairs = 0

    # iterate over all ranges and their indices
    for i in range(0, len(ranges), 2):
        range1, range2 = ranges[i], ranges[i+1]
        # print(f"{range1=} and {range2=}")
        if is_fully_contained(range1, range2, level=level):
            num_pairs += 1
            # print(f"{num_pairs=}")

    return num_pairs


def solve(input_str, level=1):
    # parse the input string into a list of ranges
    ranges = parse_input(input_str)

    # return the number of fully contained pairs
    return num_fully_contained_pairs(ranges, level=level)


# small test
input_str = '2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8'
res = solve(input_str, level=LEVEL)
ans = 2 if LEVEL == 1 else 4
assert(res == ans), f"Should be {ans=}, instead got {res=}"


with open('input.txt', 'r') as f:
    input_str = ''.join(f.readlines())
res = solve(input_str, level=LEVEL)
print(f"{res=}")

