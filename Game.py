import pygame

from Render import Render
from Sprite import *
from player import Player
from RayCaster import RayCaster
from Map import *
from MiniMap import MiniMap
from Grid import Grid
import Settings


class Game:

    def __init__(self):

        self.armour = None
        self.sprite = None
        pygame.init()

        pygame.display.set_caption("Ray-Caster")

        # Fullscreen display
        self.screen = pygame.display.set_mode(
            (1920, 1080),
            pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF
        )

        # Internal low resolution framebuffer
        self.render_surface = pygame.Surface(
            (Settings.RENDER_WIDTH, Settings.RENDER_HEIGHT)
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 24)

        self.running = True

        self.render = None
        self.raycaster = None
        self.player = None
        self.grid = None

        self.initialize_world()

    def initialize_world(self):

        world_rect = pygame.Rect(
            0,
            0,
            Settings.TILE_HORIZONTAL_COUNT * Settings.TILE_SIZE,
            Settings.TILE_VERTICAL_COUNT * Settings.TILE_SIZE
        )

        self.grid = Grid(world_rect, Settings.TILE_SIZE)

        self.grid.set_map(get_map())

        self.player = Player(world_rect, 0, self.grid)

        self.raycaster = RayCaster(self.player)

        self.render = Render(
            self.render_surface,
            self.grid,
            MiniMap(),
            self.raycaster.rays,
            self.player
        )

        self.sprite = Sprite(
            400,
            400,
            12
        )

        self.armour = Sprite(
            500,
            602,
            1
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

        # Clear framebuffer
        self.render_surface.fill((0, 0, 0))

        # Render world
        self.render.render()

        for i in range(len(Renderable.renderables) - 1):
            for j in range(i + 1, len(Renderable.renderables)):
                if Renderable.renderables[i].distance_from_player < Renderable.renderables[j].distance_from_player:
                    Renderable.renderables[i], Renderable.renderables[j] = Renderable.renderables[j], Renderable.renderables[i]

        for obj in Renderable.renderables:
            obj.render(self.render, self.player, self.render.textures)

        self.render.present_framebuffer()

        # Render FPS
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

        scaled_surface = pygame.transform.scale(
            self.render_surface,
            self.screen.get_size()
        )

        self.screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    def run(self):

        while self.running:

            # Cap FPS
            self.clock.tick(60)

            self.handle_events()

            self.update()

            self.render_scene()

            self.present()

        pygame.quit()
