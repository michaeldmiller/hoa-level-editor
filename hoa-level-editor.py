# Hero of Aeboria Level Editor, version 0.1.1

# changelog: adds ability to scroll left and right and ability to add new
# terrain blocks by pressing the mouse and "a" key


# import modules
import sys
import pygame
from pygame.locals import *
import os
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
        self.background = True
        self.terrain_corners = []
        self.new_game()

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

        # add text feedback holder
        self.text_surface = True

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

        # get key presses
        keys = pygame.key.get_pressed()

        # get mouse characteristics
        mouse_presses = pygame.mouse.get_pressed()
        mouse_down = False
        if True in mouse_presses:
            mouse_down = True
        mouse_position = pygame.mouse.get_pos()

        # move terrain left and right if those keys are pressed
        if keys[K_LEFT]:
            for all_terrain in self.terrain:
                all_terrain.position.x -= 5
        if keys[K_RIGHT]:
            for all_terrain in self.terrain:
                all_terrain.position.x += 5

        # add to terrain corners list
        if keys[K_a] and mouse_down:
            if len(self.terrain_corners) < 2:
                if mouse_position not in self.terrain_corners:
                    self.terrain_corners.append(mouse_position)
            # else:
            #     if mouse_position not in self.terrain_corners:
            #         del self.terrain_corners[0]
            #         self.terrain_corners.append(mouse_position)

        # clear terrain corners list
        if keys[K_c]:
            self.terrain_corners = []

        # add new terrain block
        if len(self.terrain_corners) == 2:
            # find which mouse point is the left one
            if self.terrain_corners[1][0] < self.terrain_corners[0][0]:
                left_index, right_index = 1, 0
            else:
                left_index, right_index = 0, 1

            # find which mouse point is the top one
            if self.terrain_corners[1][1] < self.terrain_corners[0][1]:
                top_index, bottom_index = 1, 0
            else:
                top_index, bottom_index = 0, 1

            x_val = self.terrain_corners[left_index][0]
            y_val = self.terrain_corners[bottom_index][1]
            w_val = self.terrain_corners[right_index][0] - self.terrain_corners[left_index][0]
            h_val = self.terrain_corners[bottom_index][1] - self.terrain_corners[top_index][1]

            terrain_piece = TerrainElement(x_val, y_val, w_val, h_val)
            self.all_sprites.add(terrain_piece)
            self.terrain.add(terrain_piece)
            self.terrain_corners = []

        text_surface = self.font.render(str(self.terrain_corners), True, (0, 0, 0))
        self.screen.blit(text_surface, (40, 50))

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
