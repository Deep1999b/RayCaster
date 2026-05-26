import pygame

from Render import Render
from player import Player
from RayCaster import RayCaster
from Map import Map
from MiniMap import MiniMap
from Grid import Grid
import Settings


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Ray-Caster")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.running = True

        self.render_surface = pygame.Surface(
            (Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT)
        )

        self.target_rect = self.calculate_render_rect()

        self.initialize_world()

    def calculate_render_rect(self):
        screen_rect = self.screen.get_rect()

        src_ratio = Settings.RENDER_WIDTH / Settings.RENDER_HEIGHT
        dst_ratio = screen_rect.width / screen_rect.height

        if dst_ratio > src_ratio:
            scale_height = screen_rect.height
            scale_width = int(scale_height * src_ratio)

            scale_x = (screen_rect.width - scale_width) // 2
            scale_y = 0

        else:
            scale_width = screen_rect.width
            scale_height = int(scale_width / src_ratio)

            scale_x = 0
            scale_y = (screen_rect.height - scale_height) // 2

        return pygame.Rect(
            scale_x,
            scale_y,
            scale_width,
            scale_height
        )

    def initialize_world(self):
        world_rect = pygame.Rect(
            0,
            0,
            Settings.TILE_HORIZONTAL_COUNT * Settings.TILE_SIZE,
            Settings.TILE_VERTICAL_COUNT * Settings.TILE_SIZE
        )

        self.grid = Grid(world_rect, Settings.TILE_SIZE)

        self.map = Map(world_rect)
        self.grid.set_map(self.map.get_map())

        self.minimap = MiniMap(world_rect)

        self.player = Player(
            world_rect,
            0,
            self.render_surface,
            self.grid
        )

        self.raycaster = RayCaster(self.player)

        self.render = Render(
            self.render_surface,
            self.grid,
            self.minimap,
            self.raycaster.rays,
            self.player
        )

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.player.Update()
        self.raycaster.cast_all_rays()

    def render_scene(self):
        self.render_surface.fill("black")

        self.render.render()

        self.render_fps()

    def render_fps(self):
        fps = int(self.clock.get_fps())

        fps_text = self.font.render(
            f"FPS: {fps}",
            True,
            (255, 255, 255)
        )

        fps_rect = fps_text.get_rect(
            topright=(Settings.RENDER_WIDTH - 20, 20)
        )

        self.render_surface.blit(fps_text, fps_rect)

    def present(self):
        self.screen.fill("black")

        scaled_surface = pygame.transform.scale(
            self.render_surface,
            self.target_rect.size
        )

        self.screen.blit(scaled_surface, self.target_rect)

        pygame.display.flip()

    def run(self):
        while self.running:

            self.clock.tick(60)

            self.handle_events()

            self.update()

            self.render_scene()

            self.present()

        pygame.quit()