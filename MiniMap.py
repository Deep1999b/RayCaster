from Grid import*
import pygame

import Settings

class MiniMap:
    def __init__(self):

        self.cell_size = int(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR)