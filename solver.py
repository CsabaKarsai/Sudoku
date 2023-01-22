from random import shuffle, sample
from itertools import product


def print_grid(grid):
    """Prints the 9x9 sudoku grid in a human-readable format.

    Args:
        grid (list of lists): grid to be printet
    """
    for x in range(0, 9):
        if x % 3 == 0 and x != 0:
            print("- - - - - - - - - - -")
        for y in range(0, 9):
            if y % 3 == 0 and y != 0:
                print("| ", end="")
            if y == 8:
                print(grid[x][y])
            else:
                print(str(grid[x][y]) + " ", end="")


def check(grid, x, y, candidate):
    """Checks whether the candidate number could be put at coordinates (x,y)

    Args:
        grid (list of lists): The Sudoku grid/board to be checked against
        x (int): Row number
        y (int): Column number
        candidate (int): Candidate number to be checked

    Returns:
        boolean: True, if candidate number can be put at coordinates (x,y)
    """
    if check_row(grid, x, candidate) == True:
        return False
    elif check_column(grid, y, candidate) == True:
        return False
    elif check_block(grid, x, y, candidate) == True:
        return False
    return True


def check_row(grid, x, candidate):
    """Checks if a row has a number equal to candidate

    Args:
        grid (list of lists): Sudoku Grid/Board to be checked against
        x (int): Row number
        candidate (int): Candidate number to be checked

    Returns:
        boolean: True, if row has a number equal to candidate
    """
    for i in range(9):
        if grid[x][i] == candidate:
            return True


def check_column(grid, y, candidate):
    """Checks if the column y has a number equal to candidate

    Args:
        grid (list of lists): Sudoku grid/board to be checked against
        y (int): Column number
        candidate (int): Candidate number to be checked

    Returns:
        boolean: True, if column has a number equal to candidate
    """
    for i in range(9):
        if grid[i][y] == candidate:
            return True


def compute_upper_corner_coordinates(x, y):
    """Computes the coordinates of the upper left corner of the 3x3 block cell (x, y) is in

    Args:
        x (int): X-coordinate of cell (row number)
        y (int): Y-coordinate of cell (column number)

    Returns:
        tuple of int: Tuple of computed coordinates
    """
    block_x = (x // 3) * 3
    block_y = (y // 3) * 3
    return (block_x, block_y)


def check_block(grid, x, y, candidate):
    """Checks if the 3x3 block corresponding to position (x,y) has a number equal

    Args:
        grid (list of lists): Sudoku grid/board to be checked against
        x (int): Row number
        y (int): Column number
        candidate (int): Candidate number to be checked

    Returns:
        boolean: True, if number equal to candidate has been found in 3x3 block
    """
    # compute coordinates of 3x3 block cooresponding to cell (x, y)
    block_x, block_y = compute_upper_corner_coordinates(x, y)
    # check each position in the block
    for i in range(3):
        for j in range(3):
            if grid[block_x + i][block_y + j] == candidate:
                return True

# Find an empty cell


def find_empty(grid):
    """Finds an empty cell in a Sudoku grid/board

    Args:
        grid (list of lists): Sudoku board/grid to be searched in

    Returns:
        tuple of int | None: Tuple of coordinates from empty cell or None if no empty cell was found
    """
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                return (x, y)
    return None


def solve(grid):
    """Solves the Sudoku grid using randomized backtracking

    Args:
        grid (list of lists): Sudoku grid to be solved

    Returns:
        boolean: True, if Sudoku grid is solvable
    """
    find = find_empty(grid)
    if not find:
        return True
    x, y = find
    candidate_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    shuffle(candidate_list)
    for candidate in candidate_list:
        if check(grid, x, y, candidate):
            grid[x][y] = candidate
            if solve(grid):
                return True
            grid[x][y] = 0
    return False


def generate_sudoku(number_of_clues):
    """Generates a valid sudoku board with a specified number of clues

    Args:
        number_of_clues (int): Number of clues (filled cells) in the resulting Sudoku board

    Returns:
        list of lists: Generated Sudoku board
    """
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    # Solve the grid in-place
    solve(grid)
    # Pick and delete random coordinates
    number_to_delete = 81 - number_of_clues
    coords_to_be_deleted = [
        divmod(
            x,
            9) for x in sample(
            range(81),
            number_to_delete)]
    for coord in coords_to_be_deleted:
        grid[coord[0]][coord[1]] = 0
    # Return finished grid
    return grid


def run(grid):
    """For testing purposes, solves and prints solution for a Sudoku grid

    Args:
        grid (list of lists): Sudoku grid to be solved
    """
    print("Input:")
    print_grid(grid)
    solvable = solve(grid)
    if solvable:
        print("Solution:")
        print_grid(grid)
    else:
        print("This Sudoku is unsolvable!")
