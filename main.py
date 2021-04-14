from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import sys

# this function parses the file input and extracts the coordinates
def parse_file(file_input):
    file_contents_in = open(file_input, "r")
    coordinates = []
    for line in file_contents_in:
        row = line.split(",")
        for value in row:
            if "x" in value and "y" in value:
                coordinates.append(value[0:4])
    return coordinates

# this function produces a matrix with an appropriate size and the reefs put in place
def produce_matrix(coordinates):
    dimension_x = 0
    dimension_y = 0
    for value in coordinates:
        x = int(value[1])
        y = int(value[3])
        if x > dimension_x:
            dimension_x = x
        if y > dimension_y:
            dimension_y = y

    matrix = [[1 for i in range(dimension_x + 1)] for j in range(dimension_y + 1)]

    # a new array is made for the reefs as we will need to use the unchanged coordinates array
    # in get_start_and_end
    reefs = coordinates.copy()

    del reefs[0]
    del reefs[len(reefs) - 1]

    for value in reefs:
        x = int(value[1])
        y = int(value[3])
        matrix[y][x] = 0

    return matrix


# this function returns a two-dimensional array for the start and end coordinates
def get_start_and_end(coordinates):
    raw_strings = []
    raw_strings.append(coordinates[0])
    raw_strings.append(coordinates[len(coordinates) - 1])

    start_and_end = []

    for value in raw_strings:
        x = int(value[1])
        y = int(value[3])
        start_and_end.append(x)
        start_and_end.append(y)

    return start_and_end

# this function calls on the other functions and uses an A* search algorithm to output a map of the correct path
def produce_map(file_input):
    coordinates = parse_file(file_input)
    matrix = produce_matrix(coordinates)

    grid = Grid(matrix=matrix)
    start_and_end = get_start_and_end(coordinates)

    start = grid.node(start_and_end[0], start_and_end[1])
    end = grid.node(start_and_end[2], start_and_end[3])

    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    file_output = file_input + ".answer"
    file_contents_out = open(file_output, "a")

    # if the length of the path is 0 we can assume that no path was found and thus return an error
    if len(path) > 0:
        file_contents_out.write(
            grid.grid_str(path=path, start=start, end=end, border=False, start_chr='S', end_chr='E', path_chr='0',
                          empty_chr='.', block_chr='x'))
    else:
        file_contents_out.write("error")

    file_contents_out.close()

try:
    produce_map(sys.argv[1])
except:
    print("An error has occurred.")

