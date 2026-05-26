from Ray import Ray
from Render import *

class RayCaster:

    def __init__(self, player):

        self.player = player
        self.rays = []

    def cast_all_rays(self):

        self.rays.clear()

        ray_angle = self.player.angle - (Settings.FOV / 2)

        col = 0

        for ray_count in range(Settings.NUM_RAYS):

            ray = Ray(ray_angle)

            ray.cast(ray_count, self.player)

            self.rays.append(ray)

            col += 1
            ray_angle = self.player.angle + math.atan((col - Settings.NUM_RAYS / 2) / Settings.DISTANCE_TO_PROJECTION_PLANE)

