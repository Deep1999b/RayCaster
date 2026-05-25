import pygame

class Sprite:
    def __init__(self, x, y, textureID):
        self.x = x
        self.y = y
        self.texture = textureID
        self.angle = 0
        self.distance_from_player = 0

class Textures:
                                
    def __init__(self):
        self.__image_path = "assets/images"
    
        self.__texture_file_names = [
                                    "redbrick.png",
                                    "armor.png",
                                    "barrel.png",
                                    "bluestone.png",
                                    "colorstone.png",
                                    "eagle.png",
                                    "graystone.png",
                                    "guard.png",
                                    "light.png",
                                    "mossystone.png",
                                    "pikuma.png",
                                    "purplestone.png",
                                    "table.png",
                                    "wood.png"
                                ]
        
        self.__textures = []
        
        self.__load_all_textures()
    
    
    def __load_all_textures(self):
        for file_name in self.__texture_file_names:
            image = pygame.image.load(f"{self.__image_path}/{file_name}").convert_alpha()
            texture = pygame.surfarray.pixels2d(image).copy().T
            self.__textures.append(texture.flatten())
    
    def get_texture(self, texture_type : int):
        return self.__textures[texture_type]