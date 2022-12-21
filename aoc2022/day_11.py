import math
import time
import sys
from typing import Dict, Any

def monkey_game(monkeys, num_rounds = 20, divide_worry_level = 3):
    # Create a list to hold the items held by each monkey
    monkey_items = [monkeys[i]['items'] for i in range(len(monkeys))]

    # Create a list of counters for each monkey
    monkey_counters = [0 for _ in range(len(monkeys))]

    m = math.prod(int(monkey['test'].split("% ")[1]) for monkey in monkeys)
    # Simulate the monkey game for 20 rounds
    for r in range(num_rounds):
        #print(f"round = {r}")
        #print(f"{monkeys=}")
        # Iterate through the monkeys
        for i, monkey in enumerate(monkeys):
            #print(f"Processing monkey {i=}")
            # Get the list of items held by this monkey
            items = monkey_items[i]

            # Process the items one by one
            #print(f"\t#items = {len(items)}")
            for item in items:
                # Perform the operation on the item
                op = monkey['op']
                # print(f"{op=}")
                tic = time.time()
                if op == "* old":
                    new_item = item * item
                else:
                    operand, constant = op.split(" ")
                    constant = int(constant)
                    if operand == "+":
                        new_item = item + constant
                    elif operand == "-":
                        new_item = item - constant
                    elif operand == "*":
                        new_item = item * constant
                    elif operand == "/":
                        new_item = item / constant
                    #new_item = eval(f"{item}{monkey['op']}")
                #print(f"new_item took: {(time.time() - tic):.3f} sec")
                # Divide the result by 3 and round down to the nearest integer
                new_item = (new_item % m) // divide_worry_level

                # Test the resulting value against the monkey's test condition
                tic = time.time()
                mod = int(monkey['test'].split("% ")[1])
                test = (new_item % mod == 0)
                #print(f"test took: {(time.time() - tic):.3f} sec")
                if test:
                    # If the test condition is true, append the item to the list of the monkey specified by the "If true" condition
                    monkey_items[monkey['if_true']].append(new_item)
                else:
                    # If the test condition is false, append the item to the list of the monkey specified by the "If false" condition
                    monkey_items[monkey['if_false']].append(new_item)


                # Increment the counter for this monkey
                monkey_counters[i] += 1

            # Clear the list of items held by this monkey
            monkey_items[i] = []

    # Return the final list of items held by each monkey and the counters for each monkey
    return monkey_items, monkey_counters


def parse_input(lines: str) -> Dict[str, Any]:

    d = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("Monkey"):
            monkey_id = int(lines[i][:-1].split(" ")[1])
            items = list(map(int, lines[i+1].split(": ")[1]. split(", ")))
            op = lines[i+2].split(" = ")[1].split("old ")[-1]
            test = "% " + lines[i+3].split("by ")[1]
            if_true_to_monkey = int(lines[i+4].split(" ")[-1])
            if_false_to_monkey = int(lines[i+5].split(" ")[-1])

            d.append({"items": items, "op": op, "test": test, "if_true": if_true_to_monkey, "if_false": if_false_to_monkey})

            i+= 7

    return d

def read_input():

    lines = [line.strip() for line in sys.stdin.readlines()]
    d = parse_input(lines)

    return d


monkeys = read_input()
monkey_items, monkey_counters = monkey_game(monkeys, num_rounds = 10_000, divide_worry_level=1)
sorted_monkey_counters = sorted(monkey_counters, reverse=True)

monkey_business = sorted_monkey_counters[0] * sorted_monkey_counters[1]

print(f"{monkey_business=}")

