import Settings
import pygame
import Map
import Grid

class Render:
    def __init__(self, screen, grid, minimap):
        self.screen = screen
        self.minimap_color = (50, 50, 50)
        
        self.grid = grid
        self.minimap = minimap
                                        
        cell_size = int(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR)
        self.minimap_rect = pygame.Rect(
                                        0, 0, 
                                        Settings.TILE_HORIZONTAL_COUNT * cell_size, 
                                        Settings.TILE_VERTICAL_COUNT * cell_size
                                        )
    
    def render(self):
        pygame.draw.rect(self.screen, self.minimap_color, self.minimap_rect)
        self.minimap.draw_minimap(self.screen, self.grid.grid)
