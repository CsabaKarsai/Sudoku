# prints the sudoku board in a readable format
def print_grid(grid):
    for x in range(0,9):
        if x % 3 == 0 and x != 0:
            print("- - - - - - - - - - -")
        for y in range(0,9):
            if y % 3 == 0 and y != 0:
                print("| ", end="")
            if y == 8:
                print(grid[x][y])
            else:
                print(str(grid[x][y]) + " ", end="")

# checks whether the candidate number could be put at position (x,y)
def check(grid, x, y, candidate):
    if check_row(grid, x, candidate) == True:
        return False
    elif check_column(grid, y, candidate) == True:
        return False
    elif check_block(grid, x, y, candidate) == True:
        return False
    return True

# checks if the row x has a number equal to candidate
def check_row(grid, x, candidate):
    for i in range(9):
        if grid[x][i] == candidate:
            return True

# check if the column y has a number equal to candidate
def check_column(grid, y, candidate):
    for i in range(9):
        if grid[i][y] == candidate:
            return True
        
# computes the coordinates of the upper left corner of the 3x3 block cell (x, y) is in
def compute_upper_corner_coordinates(x, y):
    block_x = (x // 3) * 3
    block_y = (y // 3) * 3
    return (block_x, block_y)
        
# checks if the block corresponding to position (x,y) has a number equal to candidate
def check_block(grid, x, y, candidate):
    # compute coordinates of 3x3 block cooresponding to cell (x, y)
    block_x, block_y = compute_upper_corner_coordinates(x, y)
    # check each position in the block
    for i in range(3):
        for j in range(3):
            if grid[block_x+i][block_y+j] == candidate:
                return True
    
# find an empty cell
def find_empty(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                return (x, y)
    return None
            
# solve the sudoku using backtracking
def solve(grid):
    find = find_empty(grid)
    if not find:
        return True
    x, y = find
    for candidate in range(1,10):
        if check(grid, x, y, candidate):
            grid[x][y] = candidate
            if solve(grid):
                return True
            grid[x][y] = 0
    return False      
    
# final program
def run(grid):
    print("Input:")
    print_grid(grid)
    solvable = solve(grid)
    if solvable:
        print("Solution:")
        print_grid(grid)
    else:
        print("This Sudoku is unsolvable!")