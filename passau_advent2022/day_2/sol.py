# Read the secret message from the input
secret_message = input()

# Compute the offset for each letter in the secret message
offset = 0
unveiled_message = ""
MOD = 26
for i in range(len(secret_message)):
    unveiled_message += chr(ord('a') + (offset + ord(secret_message[i])-ord('a')) % MOD)
    offset = (ord(unveiled_message[-1])-ord('a')) % MOD


# Print the unveiled message
print(unveiled_message)

