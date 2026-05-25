from Grid import*
import pygame

import Settings

class MiniMap:
    def __init__(self, world_rect):
        self.rect = world_rect

        self.cell_size = int(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR)
        
    def draw_minimap(self, surface, grid):
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] != 0:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)

                pygame.draw.rect(
                                surface,
                                color,
                                    (
                                        int(self.rect.x * Settings.MINIMAP_SCALE_FACTOR) + x * self.cell_size,
                                        int(self.rect.y * Settings.MINIMAP_SCALE_FACTOR) + y * self.cell_size,
                                        self.cell_size - 1,
                                        self.cell_size - 1
                                    )
                                )