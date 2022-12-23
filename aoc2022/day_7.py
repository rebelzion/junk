import sys

# Parse the input to create a representation of the file system
file_system = {}
current_dir = '/'
for line in sys.stdin:
    line = line.strip()
    if line[0] == '$':
        # This is a command line
        command, *args = line.split()
        if command == 'cd':
            if args[0] == '/':
                current_dir = '/'
            elif args[0] == '..':
                # Move to the parent directory
                current_dir = current_dir.rsplit('/', 1)[0]
            else:
                # Move to the specified subdirectory
                current_dir = f"{current_dir}/{args[0]}"
        elif command == 'ls':
            pass
            # Print the contents of the current directory
            # print(file_system[current_dir])
    else:
        # This is a directory or file entry
        # Split the line into elements
        elements = line.split()
        if elements[0] == 'dir':
            # This is a directory entry
            dir_name = elements[1]
            # Create the directory if it doesn't exist
            if dir_name not in file_system[current_dir]:
                file_system[current_dir][dir_name] = []
        else:
            # This is a file entry
            # Store the file size and name
            file_size = int(elements[0])
            file_name = elements[1]
            file_system[current_dir].append((file_name, file_size))

def get_total_size(directory):
    total_size = 0
    # Iterate over the files and subdirectories in the directory
    for element in directory:
        if isinstance(element, tuple):
            # This is a file, add its size to the total
            total_size += element[1]
        else:
            # This is a subdirectory, calculate its total size
            total_size += get_total_size(file_system[element])
    return total_size


# Find all directories with a total size of at most 100000
small_dirs = []
for dir_name, dir_contents in file_system.items():
    if get_total_size(dir_contents) <= 100000:
        small_dirs.append(dir_name)

# Calculate the sum of the total sizes of these directories
total_size = 0
for dir_name in small_dirs:
    total_size += get_total_size(file_system[dir_name])

print(total_size)

