# Read the input from the standard input
#inp = 'small.txt'
inp = 'input.txt'
rucksacks = [line.strip() for line in open(inp)]

# Initialize the sum of priorities to 0
sum_of_priorities = 0

lvl = 2

# Iterate over each rucksack in the input
for i in range(0, len(rucksacks), 3 if lvl == 2 else 1):

    if lvl == 1:
        rucksack = rucksacks[i]
        # Compute the common item types in the rucksack's compartments
        common_item_types = set(rucksack[:len(rucksack) // 2]) & set(rucksack[len(rucksack) // 2:])
    else:
        common_item_types = set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2])

    # Iterate over each common item type and compute its priority
    for item_type in common_item_types:
        if item_type.islower():
            # If the item type is lowercase, its priority is ord(item_type) - ord('a') + 1
            priority = ord(item_type) - ord('a') + 1
        else:
            # If the item type is uppercase, its priority is ord(item_type) - ord('A') + 27
            priority = ord(item_type) - ord('A') + 27

        # Add the priority to the sum of priorities
        sum_of_priorities += priority

# Print the sum of priorities
print(sum_of_priorities)

