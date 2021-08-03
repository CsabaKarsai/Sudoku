import pygame

WIDTH = 550
HEIGHT = 550

white = [255, 255, 255]
black = [0, 0, 0]
background_color = white

def draw_grid_lines(win):
    for i in range(10):
        thickness = 1
        if(i % 3 == 0):
            thickness = 3
        pygame.draw.line(win, black, (50 + 50 * i, 50), (50 + 50 * i, 500), thickness)
        pygame.draw.line(win, black, (50, 50 + 50 * i), (500, 50 + 50 * i), thickness)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    
    draw_grid_lines(win)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()