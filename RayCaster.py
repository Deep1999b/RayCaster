import math
from turtle import color
import pygame
import numpy

from Ray import Ray
import Settings
from Textures import *
from Grid import *

class RayCaster:

    def __init__(self, player):

        self.player = player
        self.rays = []
        self.textures = Textures()

        self.surface = pygame.Surface(
            (Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT)
        )


        # Initialize as a 1D linear array
        self.frame_buffer = numpy.zeros(Settings.RENDER_WIDTH * Settings.RENDER_HEIGHT, dtype=numpy.uint32)
                    
        self.distance_to_projection_plane = ((Settings.RENDER_WIDTH / 2) / math.tan(Settings.FOV / 2))

    def cast_all_rays(self):

        self.rays.clear()

        ray_angle = self.player.angle - (Settings.FOV / 2)

        col = 0

        for ray_count in range(Settings.NUM_RAYS):

            ray = Ray(ray_angle)

            ray.cast(ray_count, self.player)

            self.rays.append(ray)

            col += 1
            ray_angle = self.player.angle + math.atan((col - Settings.NUM_RAYS / 2) / self.distance_to_projection_plane)

    def render_3D_projected_walls(self, screen):

        # Create a 2D view for easier indexing during strip rendering
        # Pygame's blit_array expects (width, height)
        frame_2d = self.frame_buffer.reshape((Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT))

        # Fast background fill: Ceiling and Floor
        # Top half (Ceiling)
        frame_2d[:, :Settings.RENDER_HEIGHT // 2] = 0xFF36454F
        # Bottom half (Floor)
        frame_2d[:, Settings.RENDER_HEIGHT // 2:] = 0xFF06402B

        for i, ray in enumerate(self.rays):

            
            distance_in_world = ray.wall_hit_distance

            corrected_distance = (distance_in_world * math.cos(ray.ray_angle - self.player.angle))

            corrected_distance = max(corrected_distance, 0.0001)

            wall_strip_height = int((Settings.TILE_SIZE / corrected_distance) * self.distance_to_projection_plane)

            actual_wall_top = int((Settings.RENDER_HEIGHT / 2) - (wall_strip_height / 2))

            actual_wall_bottom = int((Settings.RENDER_HEIGHT / 2) + (wall_strip_height / 2))

            wall_top = max(0, actual_wall_top)

            wall_bottom = min(Settings.RENDER_HEIGHT, actual_wall_bottom)

            self.texture_buffer = self.textures.get_texture(max(0, ray.hit_texture - 1))

            x_start = i * Settings.WALL_WIDTH
            x_end = x_start + Settings.WALL_WIDTH

            # Vectorized texture mapping for the strip
            y_indices = numpy.arange(wall_top, wall_bottom)
            texture_offset_Y = ((y_indices - actual_wall_top) * Settings.TEXTURE_HEIGHT / wall_strip_height).astype(numpy.int32)
            texture_offset_Y = numpy.clip(texture_offset_Y, 0, Settings.TEXTURE_HEIGHT - 1)
            
            # Correct for minimap scale factor in texture sampling
            if ray.was_hit_vertical:
                texture_offset_x = (ray.wall_hit_y % self.player.grid.cell_size)
            else:
                texture_offset_x = (ray.wall_hit_x % self.player.grid.cell_size)
                
            texture_offset_x = int(texture_offset_x * Settings.TEXTURE_WIDTH / self.player.grid.cell_size)
            texture_offset_x = max(0, min(texture_offset_x, Settings.TEXTURE_WIDTH - 1))
            
            if ray.was_hit_vertical:
                self.texture_buffer = self.texture_buffer
            else:
                self.texture_buffer = (self.texture_buffer >> 1) & 0x7F7F7F
            
            # Extract colors and assign to the 2D view (broadcasts across x_start:x_end)
            colors = self.texture_buffer[texture_offset_Y * Settings.TEXTURE_WIDTH + texture_offset_x]
            frame_2d[x_start:x_end, wall_top:wall_bottom] = colors

        pygame.surfarray.blit_array(
            self.surface,
            frame_2d
        )

        screen.blit(self.surface, (0, 0))