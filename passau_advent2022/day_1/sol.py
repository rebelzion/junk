# Read the number of passes from the input
n = int(input())

# Read the original and output strings from the input
original = input()
output = input()

# Compute the mask that will be used to flip the bits
mask = (1 << n) - 1

# Flip the bits in the original string using the mask
original = "".join(str((int(ch) ^ mask) % 2) for ch in original)

# Compare the resulting string to the output string
if original == output:
    print("Deletion successful.")
else:
    print("Deletion failed.")

