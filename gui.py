import pygame
import time
from solver import *

WIDTH = 550
HEIGHT = 600
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BACKGROUND_COLOR = WHITE
NUMBER_OF_CLUES = 30


class Cell:
    """One cell of the 9x9 Sudoku grid
    """

    def __init__(self, value, row, col):
        """Constructor for the cell class

        Args:
            value (int): Value (number) inside the cell
            row (int): Row number of the cell
            col (int): Column number of the cell
        """
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = 50
        self.height = 50
        self.selected = False

    def draw(self, win):
        """Draws a single cell

        Args:
            win (pygame window): Window to draw the cell on
        """
        fnt = pygame.font.SysFont("comicsans", 35)
        fnt_small = pygame.font.SysFont("comicsans", 30)
        x, y = (50 + self.col * 50, 50 + self.row * 50)
        # Draw a temporal value in upper left corner of a cell
        if self.temp != 0 and self.value == 0:
            temp = fnt_small.render(str(self.temp), True, (128, 128, 128))
            win.blit(temp, (x + 5, y + 5))
        # Draw value of a cell
        elif not (self.value == 0):
            temp = fnt.render(str(self.value), True, (0, 0, 0))
            win.blit(temp, (x + (25 - temp.get_width() / 2),
                     y + (25 - temp.get_height() / 2)))
        if self.selected:
            pygame.draw.rect(win, RED, (x, y, 50, 50), 3)

    def set_value(self, val):
        """Sets the value of the cell

        Args:
            val (int): Value (number inside) of a cell
        """
        self.value = val

    def set_temp(self, val):
        """Sets a temporary value for a cell (little grey number in upper corner)

        Args:
            val (int): Temporary value of the cell
        """
        self.temp = val


class Grid:
    """Grid for the 9x9 Sudoku board the game will be played on
    """

    def __init__(self, grid):
        """Constructor for the grid class

        Args:
            grid (list of lists): Sudoku grid
        """
        self.grid = grid
        self.cells = [[Cell(self.grid[i][j], i, j)
                       for j in range(9)] for i in range(9)]
        self.modified = None
        self.selected = None

    def update_modified(self):
        """Updates the model which will be sent to solver to solve
        """
        self.modified = [
            [self.cells[i][j].value for j in range(9)] for i in range(9)]

    def put(self, val):
        """Checks if putting a value in the selected cell is possible

        Args:
            val (int): Value to be checked for the cell

        Returns:
            boolean: True, if a solution for the board with the new value exists
        """
        row, col = self.selected
        # Check for valid value already present in cell
        if self.cells[row][col].value == 0:
            self.update_modified()
            # Check if rows, columns and 3x3 blocks allow for a placement of
            # this value in the cell
            check_grid = check(self.modified, row, col, val)
            # Place the value in the Cell
            self.cells[row][col].set_value(val)
            self.update_modified()
            # Check if solution for modified grid exists
            solvable = solve(self.modified)
            if check_grid and solvable:
                return True
            # Reset the cell
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update_modified()
                return False

    def note(self, val):
        """Notes a number in the upper left corner of a cell

        Args:
            val (int): Value to be set as a temporary value
        """
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self, win):
        """Draws the Sudoku grid

        Args:
            win (pygame windows): Window to draw the grid on
        """
        # Draw grid lines
        draw_grid_lines(win)
        # Draw cells
        draw_cells(win, self.cells)

    def select(self, row, col):
        """Selects a cell at a given row and column

        Args:
            row (int): Row number of the cell to be selected
            col (_type_): Column number of the cell to be selected
        """
        # Reset all other
        for i in range(9):
            for j in range(9):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        """Clears the selected cell of a noted value
        """
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def click(self, pos):
        """Converts the mouse coordinates to grid coordinates

        Args:
            pos (mouse position): Mouse position

        Returns:
            tuple of int | None: Tuple of grid coordinates or None if outside the game
        """
        if (51 < pos[0] < 500) and (50 < pos[1] < 500):
            x = (pos[0] // 50) - 1
            y = (pos[1] // 50) - 1
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        """Checks if the Sudoku is completed

        Returns:
            boolean: True, if the game is completed
        """
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False
        return True


def draw_grid_lines(win):
    """Draws the grid lines for the Sudoku board

    Args:
        win (pygame window): Window the lines a drawn on
    """
    for i in range(10):
        thickness = 1
        if (i % 3 == 0):
            thickness = 3
        pygame.draw.line(win, BLACK, (50 + 50 * i, 50),
                         (50 + 50 * i, 500), thickness)
        pygame.draw.line(win, BLACK, (50, 50 + 50 * i),
                         (500, 50 + 50 * i), thickness)


def draw_cells(win, cells):
    """Draws the values for each cell

    Args:
        win (pygame window): Windows the cells are drawn on
        cells (Cell): Cell that will be drawn
    """
    for i in range(9):
        for j in range(9):
            cells[i][j].draw(win)


def redraw_window(win, grid, time, text):
    """Updates the content of the window to be displayed

    Args:
        win (pygame window): Window to be displayed
        grid (Grid): Sudoku grid
        time (python time): Elapsed play time
        text (String): Text to be shown in the window
    """
    win.fill(WHITE)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 30)
    time_to_show = fnt.render("Time: " + format_time(time), True, BLACK)
    win.blit(time_to_show, (WIDTH - 500, HEIGHT - 80))
    # Draw text if user presses return key
    fnt = pygame.font.SysFont("comicsans", 30)
    text_to_show = fnt.render(text, True, BLACK)
    win.blit(text_to_show, (WIDTH - 500, HEIGHT - 45))
    # Draw grid
    grid.draw(win)


def format_time(time_in_secs):
    """Returns the time in hours:minutes:seconds format

    Args:
        time_in_secs (int): Time in seconds

    Returns:
        python time: Time in hours:minutes:seconds format
    """
    seconds = time_in_secs % 60
    minutes = time_in_secs // 60
    hours = minutes // 60
    time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
    return time


def main():
    """Runs the game
    """
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 35)
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    grid = Grid(generate_sudoku(NUMBER_OF_CLUES))
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
                            text = "Your guess for cell (%d,%d) was correct!" % (
                                i, j)
                        else:
                            if grid.cells[i][j].value == 0:
                                text = "Your guess for cell (%d,%d) was wrong." % (
                                    i, j)
                        key = None

                        if grid.is_finished():
                            text = "Congratulations! You finished this Sudoku!"

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked[0], clicked[1])
                    key = None

        if grid.selected and key is not None:
            grid.note(key)

        redraw_window(win, grid, play_time, text)
        pygame.display.update()


if __name__ == '__main__':
    main()
