import math
from RayCaster import *
import numpy
import Settings
from Renderable import Renderable


class Sprite(Renderable):

    def __init__(self, x, y, texture_id):
        super().__init__()

        self.x = x
        self.y = y
        self.texture_id = texture_id
        self.angle = 0
        self.distance_from_player = 0
        self._texture_2d = None
        self._texture_alpha = None

    def _load_texture_cache(self, texture_manager):
        if self._texture_2d is not None and self._texture_alpha is not None:
            return

        texture = texture_manager.get_texture(self.texture_id).reshape(
            (Settings.TEXTURE_HEIGHT, Settings.TEXTURE_WIDTH)
        )
        visible_mask = texture_manager.get_texture_visible_mask(
            self.texture_id
        ).reshape((Settings.TEXTURE_HEIGHT, Settings.TEXTURE_WIDTH))

        self._texture_2d = texture
        self._texture_alpha = visible_mask


    def render(self, render, player, texture_manager):
        # Distance from player in world space.
        dx = self.x - player.x
        dy = self.y - player.y

        distance = math.sqrt(dx * dx + dy * dy)
        self.distance_from_player = distance

        if distance < 0.0001:
            return

        # Angle between player and sprite.
        sprite_angle = math.atan2(dy, dx) - player.angle

        if sprite_angle > math.pi:
            sprite_angle -= math.pi * 2

        if sprite_angle < -math.pi:
            sprite_angle += math.pi * 2

        # Outside FOV
        if abs(sprite_angle) > (Settings.FOV / 2):
            return

        # Use the depth along the camera direction for stable projection.
        depth = distance * math.cos(sprite_angle)

        if depth <= 0.0001:
            return

        # Projected sprite size.
        sprite_size = int((32 * Settings.DISTANCE_TO_PROJECTION_PLANE) / depth)

        if sprite_size <= 0:
            return

        # Match the current wall projection, which advances angles per ray column.
        screen_x = int((Settings.RENDER_WIDTH / 2) + (math.tan(sprite_angle) * Settings.DISTANCE_TO_PROJECTION_PLANE * Settings.WALL_WIDTH))

        # Sprite bounds.
        left = screen_x - (sprite_size // 2)
        right = screen_x + (sprite_size // 2)

        top = (Settings.RENDER_HEIGHT // 2) - (sprite_size // 2)
        bottom = top + sprite_size

        # Completely off-screen.
        if right < 0 or left >= Settings.RENDER_WIDTH:
            return

        if bottom < 0 or top >= Settings.RENDER_HEIGHT:
            return

        # Clip to screen.
        draw_left = max(0, left)
        draw_right = min(Settings.RENDER_WIDTH, right)

        draw_top = max(0, top)
        draw_bottom = min(Settings.RENDER_HEIGHT, bottom)

        draw_width = draw_right - draw_left
        draw_height = draw_bottom - draw_top

        if draw_width <= 0 or draw_height <= 0:
            return

        self._load_texture_cache(texture_manager)

        source_left = draw_left - left
        source_top = draw_top - top

        tex_x = (
            (source_left + numpy.arange(draw_width, dtype=numpy.int32))
            * Settings.TEXTURE_WIDTH
        ) // sprite_size

        tex_y = (
            (source_top + numpy.arange(draw_height, dtype=numpy.int32))
            * Settings.TEXTURE_HEIGHT
        ) // sprite_size

        tex_x = numpy.clip(
            tex_x,
            0,
            Settings.TEXTURE_WIDTH - 1
        )
        tex_y = numpy.clip(
            tex_y,
            0,
            Settings.TEXTURE_HEIGHT - 1
        )

        for screen_x in range(draw_width):

            ray_index = (draw_left + screen_x) // Settings.WALL_WIDTH

            if ray_index < 0 or ray_index >= len(RayCaster.rays):
                continue

            texture_x = tex_x[screen_x]

            texture_column = self._texture_2d[tex_y, texture_x]
            opaque_mask = self._texture_alpha[tex_y, texture_x]

            if (
                    numpy.any(opaque_mask)
                    and distance < RayCaster.rays[ray_index].wall_hit_distance
            ):
                framebuffer_column = render.game_frame_2d[
                    draw_left + screen_x,
                    draw_top:draw_bottom
                ]

                framebuffer_column[opaque_mask] = texture_column[opaque_mask]

    def calculate_distance_between_sprite_and_player(self, player):
        distance_from_player = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        return distance_from_player


    def calculate_angle_between_sprite_and_player(self, player):
        angle = math.atan2(self.y - player.y, self.x - player.x) - player.get_normalized_angle()

        if angle > math.pi:
            angle -= (math.pi * 2.0)
        if angle < -math.pi:
            angle += (math.pi * 2.0)

        return angle

    def is_renderable(self, player):
        return self.calculate_angle_between_sprite_and_player(player) < (Settings.FOV / 2.0)

