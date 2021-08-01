#representation of a sudoku board, list of rows
grid1 = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

grid2 = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

#prints the sudoku board in a redable format
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

#checks whether the candidate number could be put at position (x,y)
#x: 0-8
#y: 0-8
#number: 1-9
def check(grid, x, y, candidate):
    if check_row(grid, x, candidate) == False:
        return False
    elif check_column(grid, y, candidate) == False:
        return False
    elif check_block(grid, x, y, candidate) == False:
        return False
    return True

#checks if the row x has a number equal to candidate
def check_row(grid, x, candidate):
    for i in range(0,9):
        if grid[x][i] == candidate:
            return False

#check if the column y has a number equal to candidate
def check_column(grid, y, candidate):
    for i in range(0,9):
        if grid[i][y] == candidate:
            return False
        
#checks if the block corresponding to position (x,y) has a number equal to candidate
def check_block(grid, x, y, candidate):
    #compute coordinates (x0,y0) of upper left corner of block corresponding to position (x,y)
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    #check each position in the block
    for i in range(0,3):
        for j in range(0,3):
            if grid[x0+i][y0+j] == candidate:
                return False

#tests
print_grid(grid2)
print("-----")
print(check(grid2, 8, 6, 1))
print(check(grid2, 6, 8, 1))