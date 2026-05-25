import pygame

class Grid:

    def __init__(self, transform_rect : pygame.Rect, cell_size):
        self.rect = transform_rect
        self.cell_size = int(cell_size)

        self.grid = [
            [0 for _ in range(transform_rect.width // self.cell_size)]
            for _ in range(transform_rect.height // self.cell_size)
        ]
    
    def get_Cell_Type(self, x, y):
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)

        if 0 <= grid_x < len(self.grid[0]) and 0 <= grid_y < len(self.grid):
            return self.grid[grid_y][grid_x]
        return 1



    def set_map(self, tiles):
        self.grid =  tiles