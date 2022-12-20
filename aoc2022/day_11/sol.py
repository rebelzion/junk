def monkey_game(monkeys):
    # Create a list to hold the items held by each monkey
    monkey_items = [[] for _ in range(len(monkeys))]

    # Create a list of counters for each monkey
    monkey_counters = [0 for _ in range(len(monkeys))]

    # Simulate the monkey game for 20 rounds
    for _ in range(20):
        # Keep track of the number of items thrown during each round
        items_thrown = len(monkeys[0]['items'])

        # Simulate the monkey game
        while items_thrown > 0:
            # Reset the number of items thrown during this round
            items_thrown = 0

            # Iterate through the monkeys
            for i, monkey in enumerate(monkeys):
                # Get the list of items held by this monkey
                items = monkey_items[i]

                # Process the items one by one
                for item in items:
                    # Perform the operation on the item
                    new_item = eval(f"{item}{monkey['op']}")

                    # Divide the result by 3 and round down to the nearest integer
                    new_item = new_item // 3

                    # Test the resulting value against the monkey's test condition
                    if eval(f"{new_item}{monkey['test']}"):
                        # If the test condition is true, append the item to the list of the monkey specified by the "If true" condition
                        monkey_items[monkey['if_true']].append(new_item)
                    else:
                        # If the test condition is false, append the item to the list of the monkey specified by the "If false" condition
                        monkey_items[monkey['if_false']].append(new_item)

                    # Increment the number of items thrown during this round
                    items_thrown += 1

                    # Increment the counter for this monkey
                    monkey_counters[i] += 1

                # Clear the list of items held by this monkey
                monkey_items[i] = []

    # Return the final list of items held by each monkey and the counters for each monkey
    return monkey_items, monkey_counters


def parse_monkey(lines: str, line_idx: int) -> Dict[str, Any]:

    d = {}
    i = line_idx
    while i < len(lines):
        if line.startswith("Monkey"):
            monkey_id = int(line[:-1].split(" ")[1])
            d["id"] = monkey_id
        elif "Starting items" in line:
            items =



def read_input():

    lines = line.strip() for line in sys.stdin.readlines()]





# Test the function
monkeys = [
    {'items': [79, 98], 'op': '* 19', 'test': '% 23 == 0', 'if_true': 2, 'if_false': 3},
    {'items': [54, 65, 75, 74], 'op': '+ 6', 'test': '% 19 == 0', 'if_true': 2, 'if_false': 0},
    {'items': [79, 60, 97], 'op': '* old', 'test': '% 13 == 0', 'if_true': 1, 'if_false': 3},
    {'items': [74], 'op': '+ 3', 'test': '% 17 == 0', 'if_true': 0, 'if_false': 1}
]
print(monkey_game(monkeys))

