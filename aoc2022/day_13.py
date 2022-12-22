import json
from utils import read_input
import functools


def count_right_order_pairs_gpt(packet_pairs):
    def compare(left, right):
        # If both values are integers, compare them
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                return None
        # If both values are lists, compare their elements recursively
        if isinstance(left, list) and isinstance(right, list):
            # Zip and iterate through the two lists in parallel
            for l, r in zip(left, right):
                result = compare(l, r)
                # If the comparison returned a result, return it
                if result is not None:
                    return result
            if len(left) < len(right):
                return True
            elif len(left) > len(right):
                return False
            else:
                return None
        # If one value is an integer and the other is a list, convert the integer to a list and retry the comparison
        if isinstance(left, int):
            left = [left]
        else:
            right = [right]
        return compare(left, right)

    # Iterate through the packet pairs and count the ones that are in the right order
    right_order_count = 0
    for i, (left, right) in enumerate(packet_pairs):
        result = compare(left, right)
        if result is not None and result:
            right_order_count += i + 1
    return right_order_count


def compare(left, right):

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, list) and isinstance(right, list):
        # Zip and iterate through the two lists in parallel
        for l, r in zip(left, right):
            result = compare(l, r)
            if result is not None:
                return result
        if len(left) == len(right):
            return None
        return len(left) < len(right)

    # If one value is an integer and the other is a list, convert the integer to a list and retry the comparison
    if isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]
    return compare(left, right)


def cmp(a, b):
  res = compare(a,b)
  if res is None:
    return 0
  return -1 if res else 1

def count_right_order_pairs(packet_pairs):
    # Iterate through the packet pairs and count the ones that are in the right order
    right_order_count = 0
    for i, (left, right) in enumerate(packet_pairs):
        result = compare(left, right)
        # print(f"Pair {i+1}: {result}")
        if result:
            right_order_count += i+1
    return right_order_count



def solve(packet_pairs):

    packets = [p for p in packet_pairs for p in p]
    packets.append([[2]])
    packets.append([[6]])
    # Sort the list using the sorted function
    sorted_packets = sorted(packets, key=functools.cmp_to_key(cmp))
    # for i, sp in enumerate(sorted_packets):
    #   print(i+1, '->' , sp)
    # Find the indices of the divider packets
    divider1_index = sorted_packets.index([[2]])
    divider2_index = sorted_packets.index([[6]])
    # Return the product of the indices of the divider packets
    return (divider1_index+1) * (divider2_index+1)


def test(packet_pairs):
    expected = 13
    output = count_right_order_pairs(packet_pairs)
    output_gpt = count_right_order_pairs_gpt(packet_pairs)
    assert output == expected, f"Expecting {expected}, got {output}"
    assert output_gpt == expected, f"Expecting {expected}, got {output}"


def parse_input(inp):

    packet_pairs = []
    for i in range(0, len(inp), 2):
        packet_pairs.append((json.loads(inp[i]), json.loads(inp[i+1])))
    return packet_pairs


if __name__ == '__main__':

    test(
        packet_pairs=[([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
                      ([[1], [2, 3, 4]], [[1], 4]),
                      ([9], [[8, 7, 6]]),
                      ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
                      ([7, 7, 7, 7], [7, 7, 7]),
                      ([], [3]),
                      ([[[]]], [[]]),
                      ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                       [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
                      ]
    )

    inp = read_input(ignore_empty_lines=True)
    packet_pairs = parse_input(inp)
    output = count_right_order_pairs(packet_pairs)
    print(output)

    print(solve(packet_pairs))
