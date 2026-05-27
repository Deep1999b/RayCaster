import math
from operator import pos

import pygame
import Settings

class Player:
    def __init__(self, rect: pygame.Rect, angle, grid):
        self.grid = grid
        self.x = rect.x + rect.width / 2
        self.y = rect.y + rect.height / 2
        self.angle = math.radians(angle)
        
        self.forward_speed = 2.0
        self.strafe_speed = 1.0
        self.radius = 8

        self.FOV = math.radians(60)  # Field of view in radians
        
        # Lock and hide mouse for FPS/raycaster movement
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def Update(self):

        # Mouse movement (NOT mouse position)
        mouse_rel = pygame.mouse.get_rel()[0]

        # Rotate player based on mouse movement
        self.angle += mouse_rel * 0.001

        # Get direction once
        direction_x, direction_y = self.get_current_direction()

        keys = pygame.key.get_pressed()
        
        move_x = 0
        move_y = 0

        # Forward
        if keys[pygame.K_w]:
            move_x += direction_x * self.forward_speed
            move_y += direction_y * self.forward_speed

        # Backward
        if keys[pygame.K_s]:
            move_x -= direction_x * self.forward_speed
            move_y -= direction_y * self.forward_speed

        # Strafe right
        if keys[pygame.K_d]:
            move_x -= direction_y * self.strafe_speed
            move_y += direction_x * self.strafe_speed

        # Strafe left
        if keys[pygame.K_a]:
            move_x += direction_y * self.strafe_speed
            move_y -= direction_x * self.strafe_speed

        # Normalize diagonal speed so moving forward + strafing isn't 1.4x faster
        is_moving_fb = keys[pygame.K_w] or keys[pygame.K_s]
        is_moving_lr = keys[pygame.K_a] or keys[pygame.K_d]
        
        if is_moving_fb and is_moving_lr:
            move_x *= 0.7071
            move_y *= 0.7071

        if move_x != 0 or move_y != 0:
            self.move(move_x, move_y)

    def get_current_direction(self):
        return (
            math.cos(self.get_normalized_angle()),
            math.sin(self.get_normalized_angle())
        )

    def move(self, dx, dy):
        # Independent axis collision allows "sliding" along walls instead of stopping completely
        if not self.grid.get_cell_type(self.x + dx, self.y):
            self.x += dx
            pos_x = self.x
            
        if not self.grid.get_cell_type(self.x, self.y + dy):
            self.y += dy
            pos_y = self.y

    def get_normalized_angle(self):
        normalized_angle = self.angle

        if normalized_angle > math.pi:
            normalized_angle -= math.pi * 2
        if normalized_angle < -math.pi:
            normalized_angle += math.pi * 2

        return normalized_angle
