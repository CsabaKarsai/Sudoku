import pygame
import requests

WIDTH = 550
HEIGHT = 550

white = [255, 255, 255]
black = [0, 0, 0]
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

def get_grid_from_API(difficulty):
    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=" + difficulty)
    return response.json()["board"]

def draw_grid_values(win ,grid, font):
    for i in range(9):
        for j in range(9):
            if (0 < grid[i][j] < 10):
                value = font.render(str(grid[i][j]), True, black)
                win.blit(value, ((j + 1) * 50 + 20, (i + 1) * 50 + 14))
                
def redraw_window(win, board, time, strikes):
    win.fill(black)
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 35)
    text = fnt.render("Time: " + format_time(time), True, white)
    win.blit(text, (WIDTH - 200, HEIGHT - 20))
    # Draw text if input failed?
    # Draw grid and board
    board.draw(win)


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
    win.fill(background_color)
    
    draw_grid_lines(win)
    grid = get_grid_from_API(game_difficulty)
    draw_grid_values(win, grid, font)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()

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
    
    
    def grid_to_pygame_coords():
        return (50 + self.col * 50, 50 + self.row * 50)
    
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 35)
        x, y = grid_to_pygame_coords()
        if self.temp != 0 and self.value == 0:
            temp = fnt.render(str(self.temp), True, (128,128,128))
            win.blit(temp, (x+5, y+5))
        elif not(self.value == 0):
            temp = fnt.render(str(self.value), True, (0, 0, 0))
            win.blit(temp, (x + (gap/2 - temp.get_width()/2), y + (gap/2 - temp.get_height()/2)))
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)
    
    def set_value(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val
        
