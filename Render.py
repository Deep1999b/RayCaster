import Settings
import numpy
import math
from Textures import *

class Render:
    def __init__(self, screen, grid, minimap, rays, player):
        self.screen = screen
        self.rays = rays
        self.player = player
        
        self.grid = grid
        self.minimap = minimap

        cell_size = int(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR)

        self.game_buffer = numpy.zeros(Settings.RENDER_WIDTH * Settings.RENDER_HEIGHT, dtype=numpy.uint32)
        self.game_frame_2d = self.game_buffer.reshape((Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT))

        self.minimap_buffer = numpy.zeros(
            (
                Settings.MINI_MAP_WIDTH *
                Settings.MINI_MAP_HEIGHT
            ),
            dtype=numpy.uint32
        )
        self.minimap_frame_2d = self.minimap_buffer.reshape((
                                                                Settings.MINI_MAP_WIDTH,
                                                                Settings.MINI_MAP_HEIGHT
                                                            ))

        self.textures = Textures()
        self.surface = pygame.Surface((Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT)        )
        self.minimap_surface = pygame.Surface(
            (
                    Settings.MINI_MAP_WIDTH,
                    Settings.MINI_MAP_HEIGHT
            )
        )


    def render(self):
        self.render_3d_projected_walls()
        self.render_minimap()

    def render_3d_projected_walls(self):
        # Fast background fill: Ceiling and Floor
        # Top half (Ceiling)
        self.game_frame_2d[:, :Settings.RENDER_HEIGHT // 2] = 0xFF36454F
        # Bottom half (Floor)
        self.game_frame_2d[:, Settings.RENDER_HEIGHT // 2:] = 0xFF06402B

        for i, ray in enumerate(self.rays):

            distance_in_world = ray.wall_hit_distance

            corrected_distance = (distance_in_world * math.cos(ray.ray_angle - self.player.angle))

            corrected_distance = max(corrected_distance, 0.0001)

            wall_strip_height = int((Settings.TILE_SIZE / corrected_distance) * Settings.DISTANCE_TO_PROJECTION_PLANE)

            original_wall_top = int((Settings.RENDER_HEIGHT / 2) - (wall_strip_height / 2))
            original_wall_bottom = int((Settings.RENDER_HEIGHT / 2) + (wall_strip_height / 2))

            wall_top = max(0, original_wall_top)
            wall_bottom = min(Settings.RENDER_HEIGHT, original_wall_bottom)

            texture_buffer = self.textures.get_texture(max(0, ray.hit_texture - 1))

            x_start = i * Settings.WALL_WIDTH
            x_end = x_start + Settings.WALL_WIDTH

            # Vectorized texture mapping for the strip
            y_indices = numpy.arange(wall_top, wall_bottom)
            texture_offset_Y = (
                    (y_indices - original_wall_top)
                    * Settings.TEXTURE_HEIGHT
                    / wall_strip_height
            ).astype(numpy.int32)
            texture_offset_Y = numpy.clip(texture_offset_Y, 0, Settings.TEXTURE_HEIGHT - 1)

            # Correct for minimap scale factor in texture sampling
            if ray.was_hit_vertical:
                texture_offset_x = (ray.wall_hit_y % self.player.grid.cell_size)
            else:
                texture_offset_x = (ray.wall_hit_x % self.player.grid.cell_size)

            texture_offset_x = int(texture_offset_x * Settings.TEXTURE_WIDTH / self.player.grid.cell_size)
            texture_offset_x = max(0, min(texture_offset_x, Settings.TEXTURE_WIDTH - 1))

            if ray.was_hit_vertical:
                texture_buffer = texture_buffer
            else:
                texture_buffer = self.textures.get_dark_texture(max(0, ray.hit_texture - 1))

            # Extract colors and assign to the 2D view (broadcasts across x_start:x_end)
            colors = texture_buffer[texture_offset_Y * Settings.TEXTURE_WIDTH + texture_offset_x]
            self.game_frame_2d[x_start:x_end, wall_top:wall_bottom] = colors

        pygame.surfarray.blit_array(
            self.surface,
            self.game_frame_2d
        )

        self.screen.blit(self.surface, (0, 0))

    def render_minimap(self):
        scale = max(1, math.ceil(Settings.TILE_SIZE * Settings.MINIMAP_SCALE_FACTOR))

        # Clear minimap first
        self.minimap_frame_2d[:, :] = 0xFF222222

        for y, row in enumerate(self.grid.grid):
            for x, cell in enumerate(row):
                # Choose tile color
                if cell == 0:
                    color = 0xFF000000
                else:
                    color = 0xFFFFFFFF

                # Convert map coordinates -> minimap pixel coordinates
                x_start = x * scale
                y_start = y * scale

                x_end = x_start + scale
                y_end = y_start + scale

                # Fill the block using NumPy slicing
                self.minimap_frame_2d[
                    x_start:x_end,
                    y_start:y_end
                ] = color

        player_x = int((self.player.x / Settings.TILE_SIZE) * Settings.MINIMAP_TILE_SIZE)
        player_y = int((self.player.y / Settings.TILE_SIZE) * Settings.MINIMAP_TILE_SIZE)

        self.minimap_frame_2d[
            player_x - 2:player_x + 2,
            player_y - 2:player_y + 2
        ] = 0xFFFF0000

        pygame.surfarray.blit_array(
            self.minimap_surface,
            self.minimap_frame_2d
        )

        self.screen.blit(self.minimap_surface, (0, 0))