from collections import defaultdict
from utils import read_input


# A class to represent a node in the cave graph
class CaveNode:
    def __init__(self, x, y, has_sand=False):
        self.x = x
        self.y = y
        self.has_sand = has_sand

    def __repr__(self):
        return f"({self.x}, {self.y})"


# A class to represent the cave system
class CaveSystem:
    def __init__(self):
        self.nodes = set()  # set of all cave nodes
        self.nodes_to_markers = {}  # mapping of nodes to markers
        # adjacency list representing the edges between nodes
        self.edges = defaultdict(list)
        self.source = None  # the source of the sand

    def add_node(self, x, y, has_sand=False):
        node = CaveNode(x, y, has_sand)
        self.nodes.add((node.x, node.y))
        marker = 'o' if has_sand else '#'
        self.nodes_to_markers[(node.x, node.y)] = marker
        return node

    def add_edge(self, source, destination):
        # Get the list of coordinates between the source and destination nodes
        coordinates = self.get_coordinates_between(source, destination)

        # Add a node for each coordinate between the source and destination nodes
        for x, y in coordinates:
            self.add_node(x, y, False)
        self.edges[source].append(destination)

    def get_coordinates_between(self, source, destination):
        # If the source and destination nodes have the same x coordinate, they are aligned vertically
        if source.x == destination.x:
            # Return a list of all y coordinates between the source and destination nodes
            return [(source.x, y) for y in range(min(source.y, destination.y), max(source.y, destination.y) + 1)]
        # If the source and destination nodes have the same y coordinate, they are aligned horizontally
        elif source.y == destination.y:
            # Return a list of all x coordinates between the source and destination nodes
            return [(x, source.y) for x in range(min(source.x, destination.x), max(source.x, destination.x) + 1)]
        # If the source and destination nodes are not aligned, the edge is diagonal
        else:
            # Return a list of all coordinates between the source and destination nodes
            return [(x, y) for x in range(min(source.x, destination.x), max(source.x, destination.x) + 1) for y in range(min(source.y, destination.y), max(source.y, destination.y) + 1)]

    def __repr__(self):
        grid = self.get_grid()
        return '\n'.join([''.join(row) for row in grid])

    def get_grid(self):

        # Get the minimum and maximum x and y coordinates of the cave system
        min_x = min([node[0] for node in self.nodes])
        max_x = max([node[0] for node in self.nodes])
        min_y = min([node[1] for node in self.nodes])
        max_y = max([node[1] for node in self.nodes])

        # Create a grid of empty spaces
        grid = [["." for x in range(min_x, max_x + 1)]
                for y in range(min_y, max_y + 1)]

        # Add the source of the sand to the grid
        grid[self.source.y - min_y][self.source.x - min_x] = "+"

        # Add the nodes to the grid
        for (x,y) in self.nodes:
            marker = self.nodes_to_markers[(x, y)]
            grid[y - min_y][x - min_x] = marker
        return grid

    def set_source(self, x, y):
        self.source = self.add_node(x, y, False)
        self.nodes_to_markers[(x, y)] = '+'

    def get_extreme(self, axis, func):
        res = None
        for (x,y) in self.nodes:
          marker = self.nodes_to_markers[(x, y)]
          if marker != 'o':
            if res is None:
              res = x if axis == 0 else y
            else:
              res = func(res, x) if axis == 0 else func(res, y)
        return res

    def simulate_sand_flow(self, max_steps = None):
        # Initialize the stack for the depth-first search with the source node
        stack = [self.source]
        max_y = self.get_extreme(axis=1, func=max)

        min_x, max_x = self.get_extreme(axis=0, func=min), self.get_extreme(axis=0, func=max)
        
        self.add_edge(CaveNode(min_x-1_000, max_y+2, False), CaveNode(max_x+1_000, max_y+2, False))
        
        max_y += 2

        # While there are still nodes to process in the stack
        steps = 0
        while stack:
            steps += 1
            if max_steps is not None and steps > max_steps:
              break
            # Pop the top node from the stack
            current_node = stack.pop()
            # print(f"Processing node {current_node}")
            if current_node.y > max_y:
                # print(f"Infinite fall!")
                break

            # Check if the node below the current node is not blocked
            below_node = CaveNode(current_node.x, current_node.y + 1, False)
            if (below_node.x, below_node.y)  not in self.nodes:
                # print(self.nodes)
                # print(f"Fall down: {current_node} -> {below_node}")
                # If the node below is not blocked, add it to the stack and continue the search
                stack.append(below_node)
                continue

            # If the node below is blocked, try moving diagonally down and to the left or right
            left_below_node = CaveNode(
                current_node.x - 1, current_node.y + 1, False)
            if (left_below_node.x, left_below_node.y) not in self.nodes:
                stack.append(left_below_node)
                continue

            right_below_node = CaveNode(
                current_node.x + 1, current_node.y + 1, False)
            if (right_below_node.x, right_below_node.y)  not in self.nodes:
                stack.append(right_below_node)
                continue

            # If all three options are blocked, mark the current node as having sand and move on to the next unit of sand
            self.add_node(current_node.x, current_node.y, True)
            if current_node.y == self.source.y:
                # print(f"Sand reached source!")
                break
            stack.append(self.source)

        num_sand_units = sum([1 for (x,y) in self.nodes if self.nodes_to_markers.get((x, y), '#') == 'o'])
        return num_sand_units


def parse_input(lines):
    edges = []
    for line in lines:

        nodes = line.split(" -> ")

        for fro, to in zip(nodes, nodes[1:]):
            x1, y1 = map(int, fro.split(","))
            x2, y2 = map(int, to.split(","))
            edges.append(((x1, y1), (x2, y2)))

    return edges


if __name__ == '__main__':

    # Create a new cave system
    cave = CaveSystem()

    lines = read_input()
    edges = parse_input(lines)

    for edge in edges:
        cave.add_edge(cave.add_node(*edge[0]), cave.add_node(*edge[1]))

    # Set the source of the sand
    cave.set_source(500, 0)

    # print(cave)

    # Simulate the movement of the sand through the cave system
    num_sand_units = cave.simulate_sand_flow(max_steps = None)

    print(f"Number of sand units: {num_sand_units}")

    # print(cave)
