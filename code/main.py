import sys

INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]

# Node: OOP Model of a Node
class Node:
    # Constructor
    # A node object represents an arrow from the Project Description File
    # A node object has a position, color, and direction, which are read from the file.
    # A node object also has a lists to store its neighbors and the possible neighbor paths taken (i.e. 5S, 7S)
    # Finally, a node object knows:
    # Whether it has been visited or not (self.visited), and what the next path is (self.taken_path)
    def __init__(self, x, y, color_direction):
        self.position = x, y
        self.color, self.direction = color_direction.split('-')
        self.visited = False
        self.neighbors = []
        self.possiblePaths = []
        self.taken_path = None

    # Return True Node is a neighbor to the requesting node and False is not
    # A node is a neighbor if it's color is not the same as the requesting node's color and it hasn't been visited
    def IsNeighbor(self, color):
        if color != self.color and not self.visited:
            return True
        else:
            return False

    # Return True is a node has no neighbors, meaning it is a dead end and does not lead to the goal
    def IsDeadEnd(self):
        if not len(self.neighbors):
            return True
        return False

    # OOP Function to allow for psuedo-polymorphism in the FindNeighbors Function
    def IsBullseye(self):
        return False

    # This function prints the path that was taken from the node in the requested Format. i.e (7S)
    def PrintPathTaken(self):
        path = str(self.taken_path) + str(self.direction)
        return path

    # Enqueue all adjacent nodes (Neighbors)
    # Adjacent is defined as:
    # In the direction the Node's arrow i.e. N,S,E,W,NE,NW,SW,SE
    # Unvisited
    # Not the same color as the requesting node
    def FindNeighbors(self):
        if not self.visited:
            row, column = self.position
            i, j = switch_direction(self.direction)  # Returns a positional representation of a Node's direction.
            row = row + i
            column = column + j
            number_of_moves_in_direction = 1  # Number of Iterations in a certain direction

            # While in the bounds of the graph
            while 0 <= row <= max_row_size and 0 <= column <= max_column_size:
                # If the bullseye was found, set the taken_path number to the number of iteration in this direction
                # Append the node to the node path
                # Append the bullseye to the node path
                # Print the path
                if node_graph[row][column].IsBullseye():
                    self.taken_path = number_of_moves_in_direction
                    node_path.append(self)
                    node_path.append(node_graph[row][column])
                    for i in node_path:
                        print(i.PrintPathTaken(), end=' ')
                    writeOutput()
                    exit()

                # Else If a neighbor was found:
                # Append the neighbor to the node's neighbors list
                # Append the number of iterations to its possiblePaths list
                elif node_graph[row][column].IsNeighbor(self.color):
                    self.neighbors.append(node_graph[row][column])
                    self.possiblePaths.append(number_of_moves_in_direction)

                # Iterate
                row = row + i
                column = column + j
                number_of_moves_in_direction = number_of_moves_in_direction + 1

            # Node's neighbors have been explored and is therefore marked as visited
            self.visited = True

    # Return Node's Shortest Path Neighbor
    # Remove the neighbor from the neighbors list (For proper backtracking)
    # Set taken path to distance of the neighbor's path
    def GetNeighbor(self):
        if not len(self.neighbors):
            return "No Neighbors. Please Call IsDeadEnd before GetNeighbor"
        else:
            next_node = self.neighbors[0]
            self.taken_path = self.possiblePaths[0]
            self.neighbors.pop(0)
            self.possiblePaths.pop(0)
            return next_node

    # Print Function For Debugging
    def PrintInfo(self):
        print(
            'Position: ', self.position,
            'Color:', self.color,
            'Direction: ', self.direction,
            'Possible Paths: ', self.possiblePaths
        )
# End of Node class

# Bullseye Object
class Bullseye:
    def __init__(self, x, y):
        self.position = x, y
        self.visited = False
        self.neighbors = []

    def IsBullseye(self):
        return True

    def IsNeighbor(self):
        return self.IsBullseye()

    def PrintPathTaken(self):
        return ''
# End of Bullseye Class

# Function Returns Change in Position (row, column)
# i.e. N = (-1, 0), which means move towards the 0th row
def switch_direction(case):
    direction_case = {
        'N': (-1, 0),
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1),
        'NE': (-1, 1),
        'SE': (1, 1),
        'SW': (1, -1),
        'NW': (-1, -1)
    }
    return direction_case.get(case, "Invalid direction input")


# Function Instantiates Graph Based on Input Text File
def graphFactory():
    element_model_graph = []
    object_model_graph = []

    with open(INPUT_FILE_NAME) as f:
        element = f.readline()
        max_row, max_column = element.split(' ')
        max_row = int(max_row) - 1
        max_column = int(max_column) - 1

        for line in f:
            line = line.strip()
            line = line.split(' ')
            element_model_graph.append(line)
    i = 0
    j = 0
    for row_iter in element_model_graph:
        node_list = []
        for column_iter in row_iter:
            node_list.append(instantiateNode(column_iter, i, j))
            j = j + 1
        object_model_graph.append(node_list)
        i = i + 1
        j = 0

    return max_row, max_column, element_model_graph, object_model_graph


# Function Instantiates Node Objects and the Bullseye Objects by calling their respective constructors
def instantiateNode(string_element, row, column):
    if string_element == 'O':
        return Bullseye(row, column)
    else:
        return Node(row, column, string_element)


# Traverse the Graphs, Put Path Nodes in Path Array, Mark Visited Nodes as Visited, BackTrack if no neighbors
# Find the Neighbors of a Node
# If the node has no neighbors, it's a dead end so back track to the previous node
# If the node has neighbors, traverse to the closest neighbor and recursively repeat
def traverse(node):
    node.FindNeighbors()
    if node.IsDeadEnd():
        dead_end_nodes.append(node)
        next_node = node_path[-1]
        print("Backtracking to Previous Node: ", end='')
        next_node.PrintInfo()
        node_path.pop()
    else:
        next_node = node.GetNeighbor()
        print("Traversing to next node: ", end='')
        next_node.PrintInfo()
        node_path.append(node)
    traverse(next_node)

# Print Path To Text File
def writeOutput():
    with open(OUTPUT_FILE_NAME, 'w') as f:
        f.close()
    with open(OUTPUT_FILE_NAME, 'a') as f:
        for i in node_path:
            f.write(i.PrintPathTaken() + ' ')
        f.close()


# EXECUTION

# Instantiate Graph
max_row_size, max_column_size, text_graph, node_graph = graphFactory()

# Instantiate Node Path List and Dead End Nodes List
node_path = []
dead_end_nodes = []

# Starting Node
# Initialize the starting Node (0, 0)
# Traverse
starting_node = node_graph[0][0]
traverse(starting_node)
