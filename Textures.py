import pygame

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

            image = pygame.image.load(
                f"{self.__image_path}/{file_name}"
            ).convert_alpha()

            texture = pygame.surfarray.pixels2d(image).copy().T

            # Flatten once
            texture = texture.flatten()

            # Precompute dark texture ONCE
            dark_texture = ((texture & 0xFEFEFE) >> 1) + 0x070707

            self.__textures.append({
                "normal": texture,
                "dark": dark_texture
            })


    def get_texture(self, texture_type: int):

        return self.__textures[texture_type]["normal"]

    def get_dark_texture(self, texture_type: int):

        return self.__textures[texture_type]["dark"]