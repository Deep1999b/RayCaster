import math

import numpy

import player
from Textures import *
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

        self.sprite_buffer = numpy.zeros(Settings.TEXTURE_HEIGHT * Settings.TEXTURE_WIDTH, dtype=numpy.uint8)
        self.sprite_frame_2d = self.sprite_buffer.reshape((Settings.TEXTURE_HEIGHT, Settings.TEXTURE_WIDTH))


    def render(self, screen, player, texture):
        if self.is_renderable(player):
            sprite_height = (Settings.TEXTURE_HEIGHT * Settings.DISTANCE_TO_PROJECTION_PLANE) / self.calculate_distance_between_sprite_and_player(player)
            sprite_width = sprite_height

            sprite_top_y = (Settings.RENDER_HEIGHT / 2) - (sprite_height / 2)
            if sprite_top_y < 0:
                sprite_top_y = 0
            else:
                sprite_top_y = sprite_top_y

            sprite_bottom_y = (Settings.RENDER_HEIGHT / 2) + (sprite_height / 2)
            if sprite_bottom_y > Settings.RENDER_HEIGHT:
                sprite_bottom_y = Settings.RENDER_HEIGHT
            else:
                sprite_bottom_y = sprite_bottom_y

            sprite_angle = self.calculate_angle_between_sprite_and_player(player)
            sprite_pos_x = math.tan(sprite_angle) * Settings.DISTANCE_TO_PROJECTION_PLANE

            sprite_left_x = (Settings.RENDER_WIDTH / 2) + sprite_pos_x
            sprite_right_x = sprite_pos_x + sprite_width

            texture_buffer = texture.get_texture(self.texture_id)

        else:
            pass

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

