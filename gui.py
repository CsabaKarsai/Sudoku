import pygame
import requests
import time
from code import solve, check

# One cell of the 9x9 sudoku board where a number should be put
class Cell:
    def __init__(self, value, row, col):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = 50
        self.height = 50
        self.selected = False
    
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 35)
        x, y = (50 + self.col * 50, 50 + self.row * 50)
        # Draw a temporal value in upper left corner of a cell
        if self.temp != 0 and self.value == 0:
            temp = fnt.render(str(self.temp), True, (128,128,128))
            win.blit(temp, (x+5, y+5))
        # Draw value of a cell
        elif not(self.value == 0):
            temp = fnt.render(str(self.value), True, (0, 0, 0))
            win.blit(temp, (x + (25 - temp.get_width()/2), y + (25 - temp.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, red, (x,y, 50 ,50), 3)
    
    def set_value(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val
        
# Grid consisting of 9x9 cells
class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.cells = [[Cell(self.grid[i][j], i, j) for j in range(9)] for i in range(9)]
        self.modified = None
        self.selected = None
     
    # Updates the model which will be sent to solver to solve    
    def update_modified(self):
        self.modified = [[self.cells[i][j].value for j in range(9)] for i in range(9)]
       
    # Checks if putting a value in the selected cell is possible
    def put(self, val):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.update_modified()
            # Check if rows, columns and 3x3 blocks allow for a placement of this value in the cell
            if check(self.modified, row, col, val):
                # Place the value in the Cell
                self.cells[row][col].set_value(val)
                self.update_modified()
                # Check if solution for modified grid exists
                if solve(self.modified):
                    return True
            # Reset the cell
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update_modified()
                return False
            
    # Notes a number in the upper left corner of a cell
    def note(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    # Draws the whole grid
    def draw(self, win):
        # Draw grid lines
        draw_grid_lines(win)
        # Draw cells
        draw_cells(win, self.cells)

    # Selects a cell at a given row and column
    def select(self, row, col):
        # Reset all other
        for i in range(9):
            for j in range(9):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    # Clears the selected cell of a noted value
    def clear(self):
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    # Converts the mouse coordinates to grid coordinates
    def click(self, pos):
        if (51 < pos[0] < 500) and (50 < pos[1] < 500):
            x = (pos[0]//50) - 1
            y = (pos[1]//50) - 1
            return (int(y),int(x))
        else:
            return None

    # Checks if the Sudoku is completed
    def is_finished(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False
        return True
    
WIDTH = 550
HEIGHT = 600

white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]

background_color = white
# easy, medium, hard
game_difficulty = "easy"

def draw_grid_lines(win):
    for i in range(10):
        thickness = 1
        if(i % 3 == 0):
            thickness = 3
        pygame.draw.line(win, black, (50 + 50 * i, 50), (50 + 50 * i, 500), thickness)
        pygame.draw.line(win, black, (50, 50 + 50 * i), (500, 50 + 50 * i), thickness)
        
def draw_cells(win, cells):
    for i in range(9):
            for j in range(9):
                cells[i][j].draw(win)

def get_grid_from_API(difficulty):
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=" + difficulty)
    return response.json()["board"]

def draw_grid_values(win ,grid, font):
    for i in range(9):
        for j in range(9):
            if (0 < grid[i][j] < 10):
                value = font.render(str(grid[i][j]), True, black)
                win.blit(value, ((j + 1) * 50 + 20, (i + 1) * 50 + 14))
                
def redraw_window(win, grid, time, text):
    win.fill(white)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 30)
    time_to_show = fnt.render("Time: " + format_time(time), True, black)
    win.blit(time_to_show, (WIDTH - 500, HEIGHT - 80))
    # Draw text if user presses return key
    fnt = pygame.font.SysFont("comicsans", 30)
    text_to_show = fnt.render(text, True, black)
    win.blit(text_to_show, (WIDTH - 500, HEIGHT - 45))
    # Draw grid
    grid.draw(win)


def format_time(time_in_secs):
    seconds = time_in_secs%60
    minutes = time_in_secs//60
    hours = minutes//60
    time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
    return time

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 35)
    
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")    
    #grid = Grid(get_grid_from_API(game_difficulty))
    grid = Grid([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ])
    key = None
    run = True
    text = ""
    start = time.time()
    
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    grid.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = grid.selected
                    if grid.cells[i][j].temp != 0:
                        if grid.put(grid.cells[i][j].temp):
                            text = "Your guess for cell (%d,%d) was correct!" % (i, j)
                        else:
                            text = "Your guess for cell (%d,%d) was wrong." % (i, j)
                        key = None

                        if grid.is_finished():
                            text= "Congratulations! You finished this Sudoku!"
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None

        if grid.selected and key != None:
            grid.note(key)

        redraw_window(win, grid, play_time, text)
        pygame.display.update()

main()
pygame.quit()