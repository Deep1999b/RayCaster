from Grid import*
import pygame

import Settings

class MiniMap:
    def __init__(self, world_rect):
        self.rect = world_rect

        self.cell_size = int(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR)