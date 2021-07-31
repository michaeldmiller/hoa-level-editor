# Hero of Aeboria Level Editor, version 0.1.4
# changelog: output file will now sort blocks by starting x value, ascending. Instructions
# about saving have also been added.

# import modules
import operator
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
        self.background = True
        self.terrain_corners = []
        self.time_since_save = 0

        # instructions:
        self.instruction_1 = "To add a block, press the 'a' key and click a desired corner for a new terrain block,"
        self.instruction_2 = "     then do so again for the opposite corner. A block will then be added."
        self.instruction_3 = "To remove a block which has already been added, press the 'd' key and click the block."
        self.instruction_4 = "The blocks are constructed based on the list of corners. To clear the list, press 'c'."
        self.instruction_5 = "To save your creation to a file, press 's'. This will overwrite any previous file."
        self.instruction_6 = "Press 'h' to hide these instructions."
        self.hide_instructions = False

        self.new_game()

    def new_game(self):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.not_hero = pygame.sprite.Group()
        self.unkillable = pygame.sprite.Group()

        # initialize background
        self.background = pygame.Surface((window_x_size, window_y_size))
        background_color = (100, 100, 100)
        self.background.fill(background_color)

        self.font_big = pygame.font.SysFont("cambria.ttf", 35)
        self.font_small = pygame.font.SysFont("cambria.ttf", 25)

        self.starter_platform = TerrainElement(-200, 384, 200, 40)
        self.all_sprites.add(self.starter_platform)
        self.terrain.add(self.starter_platform)
        self.unkillable.add(self.starter_platform)

        # optional code to add previously generated terrain
        # terrain_list = []
        # for terrain_tuple in terrain_list:
        #     x_val = terrain_tuple[0]
        #     y_val = terrain_tuple[1]
        #     w_val = terrain_tuple[2]
        #     h_val = terrain_tuple[3]
        #     terrain_piece = TerrainElement(x_val, y_val, w_val, h_val)
        #     self.all_sprites.add(terrain_piece)
        #     self.terrain.add(terrain_piece)

        self.run()

    def run(self):
        while True:
            self.clock.tick(target_frame_rate)
            self.events()
            self.update()

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.time_since_save += 1

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

        # clear terrain corners list
        if keys[K_c]:
            self.terrain_corners = []

        # delete block if pressing mouse and "d" key
        if keys[K_d] and mouse_down:
            for terrain_piece in self.terrain:
                if terrain_piece.rect.collidepoint(mouse_position):
                    if terrain_piece not in self.unkillable:
                        terrain_piece.kill()

        # hide instructions if key is h
        if keys[K_h]:
            self.hide_instructions = True

        # save file if key is s
        if keys[K_s]:
            self.save_file()

        # end of user input

        # add new terrain block if applicable
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

            # get x, y, width, and height values
            x_val = self.terrain_corners[left_index][0]
            y_val = self.terrain_corners[bottom_index][1]
            w_val = self.terrain_corners[right_index][0] - self.terrain_corners[left_index][0]
            h_val = self.terrain_corners[bottom_index][1] - self.terrain_corners[top_index][1]

            # create new terrain piece and add it to relevant sprite groups
            terrain_piece = TerrainElement(x_val, y_val, w_val, h_val)
            self.all_sprites.add(terrain_piece)
            self.terrain.add(terrain_piece)

            # reset terrain_corners
            self.terrain_corners = []

        # show a text indicator of the terrain corner list
        text_surface = self.font_big.render(str(self.terrain_corners), True, (0, 0, 0))
        self.screen.blit(text_surface, (1200, 50))

        # show a text indicator of the basic instructions, if user has not hidden it
        if not self.hide_instructions:
            # create the instruction surfaces
            instructions_surface_1 = self.font_small.render(self.instruction_1, True, (0, 0, 0))
            instructions_surface_2 = self.font_small.render(self.instruction_2, True, (0, 0, 0))
            instructions_surface_3 = self.font_small.render(self.instruction_3, True, (0, 0, 0))
            instructions_surface_4 = self.font_small.render(self.instruction_4, True, (0, 0, 0))
            instructions_surface_5 = self.font_small.render(self.instruction_5, True, (0, 0, 0))
            instructions_surface_6 = self.font_small.render(self.instruction_6, True, (0, 0, 0))

            # blit the instruction surfaces
            self.screen.blit(instructions_surface_1, (20, 30))
            self.screen.blit(instructions_surface_2, (20, 55))
            self.screen.blit(instructions_surface_3, (20, 80))
            self.screen.blit(instructions_surface_4, (20, 105))
            self.screen.blit(instructions_surface_5, (20, 130))
            self.screen.blit(instructions_surface_6, (20, 155))

        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

    def save_file(self):
        """Get relative positions of all added terrain blocks and save to output file"""

        # find offset
        # offset is calculated by determining relevant x distance from the right edge
        # of the starter block, which was originally at zero. Calculating offset allows
        # for saving at any point, regardless of how much the user has shifted the terrain
        # blocks by moving the "camera" with left and right

        if self.time_since_save > 120:
            # set up starting variables
            offset = self.starter_platform.rect.right
            block_list = []
            output_file = open("terrain_design.txt", "w")

            # get all terrain block characteristics
            for output_block in self.terrain:
                block_x, block_y = str(output_block.rect.x - offset), str(output_block.rect.y + output_block.rect.height)
                block_w, block_h = str(output_block.rect.width), str(output_block.rect.height)
                block_list.append([block_x, block_y, block_w, block_h])

            # sort block list by x value
            # block_list.sort(key=lambda x: x[0])
            block_list = sorted(block_list, key=lambda x: int(x[0]))

            # write to file
            for block in block_list:
                out_line = "("
                first_three_count = 0
                while first_three_count < 3:
                    out_line += block[first_three_count] + ", "
                    first_three_count += 1
                out_line += block[3] + "),\n"
                output_file.write(out_line)

            # reset time since save
            self.time_since_save = 0


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


def x_sort(entry):
    return entry[0]


game = Game()
