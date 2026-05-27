import math
import pygame
import Settings

class Ray:
    def __init__(self, ray_angle):
        self.ray_angle = self.normalize_angle(ray_angle)
        self.wall_hit_x = 0
        self.wall_hit_y = 0
        self.wall_hit_distance = 0
        self.was_hit_vertical = False
        self.hit_texture = 0

        self.is_ray_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_ray_facing_up = not self.is_ray_facing_down
        self.is_ray_facing_right = self.ray_angle < (0.5 * math.pi) or self.ray_angle > (1.5 * math.pi)
        self.is_ray_facing_left = not self.is_ray_facing_right


    def cast(self, column_ID, player):
        tile_size = player.grid.cell_size
        min_x = player.grid.rect.x
        min_y = player.grid.rect.y
        max_x = player.grid.rect.x + player.grid.rect.width
        max_y = player.grid.rect.y + player.grid.rect.height

        x_intercept = 0
        y_intercept = 0
        x_step = 0
        y_step = 0
        
        tan_angle = math.tan(self.ray_angle)
        if abs(tan_angle) < 0.0001:
            tan_angle = 0.0001 if tan_angle >= 0 else -0.0001
        
        ##################################################
        ## Horizontal Ray-Grid Intersection Code
        ##################################################
        found_horizontal_wall_hit = False
        horizontal_wall_hit_x = 0
        horizontal_wall_hit_y = 0
        horizontal_hit_texture = 0
        
        y_intercept = math.floor(player.y / tile_size) * tile_size
        y_intercept += tile_size if self.is_ray_facing_down else 0
        
        x_intercept = player.x + (y_intercept - player.y) / tan_angle
        
        y_step = tile_size if self.is_ray_facing_down else -tile_size
        
        x_step = tile_size / tan_angle
        x_step *= -1 if ((self.is_ray_facing_left and x_step > 0) or (self.is_ray_facing_right and x_step < 0)) else 1
        
        next_horizontal_touch_x = x_intercept
        next_horizontal_touch_y = y_intercept
                    
        while (next_horizontal_touch_x >= min_x and next_horizontal_touch_x <= max_x and
               next_horizontal_touch_y >= min_y and next_horizontal_touch_y <= max_y):
            
            cell_type = player.grid.get_cell_type(next_horizontal_touch_x, next_horizontal_touch_y - (1 if self.is_ray_facing_up else 0))
            if cell_type:
                found_horizontal_wall_hit = True
                horizontal_wall_hit_x = next_horizontal_touch_x
                horizontal_wall_hit_y = next_horizontal_touch_y
                horizontal_hit_texture = cell_type
                break
            else:
                next_horizontal_touch_x += x_step
                next_horizontal_touch_y += y_step
                
                
        ###################################################
        ## Vertical Ray-Grid Intersection Code
        ###################################################
        found_vertical_wall_hit = False
        vertical_wall_hit_x = 0
        vertical_wall_hit_y = 0
        vertical_hit_texture = 0
        
        x_intercept = math.floor(player.x / tile_size) * tile_size
        x_intercept += tile_size if self.is_ray_facing_right else 0
        
        y_intercept = player.y + (x_intercept - player.x) * tan_angle
        
        x_step = tile_size if self.is_ray_facing_right else -tile_size
        
        y_step = tile_size * tan_angle
        y_step *= -1 if ((self.is_ray_facing_up and y_step > 0) or (self.is_ray_facing_down and y_step < 0)) else 1
        
        next_vertical_touch_x = x_intercept
        next_vertical_touch_y = y_intercept
            
        while (next_vertical_touch_x >= min_x and next_vertical_touch_x <= max_x and
               next_vertical_touch_y >= min_y and next_vertical_touch_y <= max_y):
            
            cell_type = player.grid.get_cell_type(next_vertical_touch_x - (1 if self.is_ray_facing_left else 0), next_vertical_touch_y)
            if (cell_type):
                found_vertical_wall_hit = True
                vertical_wall_hit_x = next_vertical_touch_x
                vertical_wall_hit_y = next_vertical_touch_y
                vertical_hit_texture = cell_type
                break
            else:
                next_vertical_touch_x += x_step
                next_vertical_touch_y += y_step
                
        horizontal_distance_between_player_and_wall = math.sqrt((horizontal_wall_hit_x - player.x) ** 2 + (horizontal_wall_hit_y - player.y) ** 2) if found_horizontal_wall_hit else float('inf')   
        vertical_distance_between_player_and_wall = math.sqrt((vertical_wall_hit_x - player.x) ** 2 + (vertical_wall_hit_y - player.y) ** 2) if found_vertical_wall_hit else float('inf')
            
        if vertical_distance_between_player_and_wall < horizontal_distance_between_player_and_wall:
            self.wall_hit_x = vertical_wall_hit_x
            self.wall_hit_y = vertical_wall_hit_y
            self.wall_hit_distance = vertical_distance_between_player_and_wall
            self.was_hit_vertical = True
            self.hit_texture = vertical_hit_texture
        else:
            self.wall_hit_x = horizontal_wall_hit_x
            self.wall_hit_y = horizontal_wall_hit_y
            self.wall_hit_distance = horizontal_distance_between_player_and_wall
            self.was_hit_vertical = False
            self.hit_texture = horizontal_hit_texture

    def render(self, player):
        pygame.draw.line(player.screen, "red", (player.x, player.y), (self.wall_hit_x, self.wall_hit_y), 1)

    def normalize_angle(self, angle):
        angle = angle % (2 * math.pi)
        if angle < 0:
            angle += 2 * math.pi
        return angle
