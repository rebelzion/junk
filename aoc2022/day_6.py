import sys

def find_start_of_packet_marker(string, k = 4):
    last_four_chars = []

    # Iterate over the characters in the string
    for i, c in enumerate(string):
        # Add the current character to the list of last four characters
        last_four_chars.append(c)

        # If the list contains more than four characters, remove the first one
        if len(last_four_chars) > k:
            last_four_chars.pop(0)

        # If the list contains four different characters, return the number of
        # characters processed so far
        if len(set(last_four_chars)) == k:
            return i + 1

    # If no start-of-packet marker is found, return -1
    return -1

LEVEL = 2

for line in sys.stdin:
    inp = line.strip()
    res = find_start_of_packet_marker(inp, k = 4 if LEVEL == 1 else 14)
    print(res)
