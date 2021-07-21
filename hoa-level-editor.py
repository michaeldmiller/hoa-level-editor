# Hero of Aeboria Level Editor, version 0.0.1

# changelog: imports Hero of Aeboria code and trims out unnecessary features


# import modules
import sys
import pygame
from pygame.locals import *
vec = pygame.math.Vector2

window_x_size = 1366
window_y_size = 768
target_frame_rate = 60

# speed = how many seconds should elapse, on average,
# between two new terrain pieces spawning
# terrain_gen_speed = 2


class Game:
    """Class to initialize and hold game loop and handle events"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_x_size, window_y_size))
        pygame.display.set_caption("Hero of Aeboria Level Editor")
        self.clock = pygame.time.Clock()
        self.new_game()
        self.background = True

    def new_game(self):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.not_hero = pygame.sprite.Group()

        # initialize background
        self.background = pygame.Surface((window_x_size, window_y_size))
        background_color = (100, 100, 100)
        self.background.fill(background_color)

        self.font = pygame.font.SysFont("cambria.ttf", 20)

        terrain_list = [(-200, 384, 250, 40),]    # starting ground
        for terrain_tuple in terrain_list:
            x_val = terrain_tuple[0]
            y_val = terrain_tuple[1]
            w_val = terrain_tuple[2]
            h_val = terrain_tuple[3]
            terrain_piece = TerrainElement(x_val, y_val, w_val, h_val)
            self.all_sprites.add(terrain_piece)
            self.terrain.add(terrain_piece)

        self.run()

    def run(self):
        while True:
            self.clock.tick(target_frame_rate)
            self.events()
            self.update()

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            # elif event.type == MOUSEBUTTONDOWN:
            #     self.first_sound.play()


class TerrainElement(pygame.sprite.Sprite):
    """Basic terrain objects to collide with"""

    def __init__(self, plat_x, plat_y, plat_w, plat_h):
        pygame.sprite.Sprite.__init__(self)

        # make all inputs integers
        plat_x = int(plat_x)
        plat_y = int(plat_y)
        plat_w = int(plat_w)
        plat_h = int(plat_h)

        self.image = pygame.Surface((plat_w, plat_h))
        color = (225, 200, 150)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        rect_x = int(plat_x + (0.5 * plat_w))
        # enable rect_y to define by top left
        # rect_y = int(plat_y + plat_h)
        self.rect.x = rect_x
        self.rect.y = plat_y
        self.position = vec(rect_x, plat_y)

    def update(self):
        self.rect.midbottom = self.position




# format for stage block dictionaries:
# name, [course object 1, course object 2, course object ...., course object x],
# [enemy 1, enemy 2, enemy ..., enemy x]
# types:
# str, list of TerrainElements

game = Game()
