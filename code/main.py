import pygame
from settings import *
from sys import exit
from random import randint
from support import import_audio
from time import time, sleep


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # player animation
        player_walk_1 = GRUNT_1_IMG
        player_walk_2 = GRUNT_2_IMG
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = GRUNT_JUMP_IMG

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(160, GROUND))
        self.gravity = 0
        self.jump_height = -20
        self.jumped_already = False

        # speech
        self.speech_history = []

    def animation_state(self):

        if self.rect.bottom < GROUND:
            self.image = self.player_jump
        else:
            self.player_index += 0.05
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        global speech_list
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND:
            self.gravity = self.jump_height  # jump
            if self.jumped_already:
                self.jumped_already = False
            else:
                self.speech_history = play_random(
                    speech_list, self.speech_history)
                self.jumped_already = True

    def apply_gravity(self):
        # applies when jumping, simulates falling
        self.gravity += 0.90
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND:
            self.rect.bottom = GROUND

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Menu:
    def __init__(self, create_level, create_secret_level):

        # screen
        self.display_surface = pygame.display.get_surface()

        # background
        self.menu_bg = MENU_IMG

        # menu messages
        self.main_font = MAIN_FONT
        self.main_msg_surf = self.main_font.render('Halo', True, '#fbfffe')
        self.main_msg_rect = self.main_msg_surf.get_rect(center=(450, 125))

        self.sec_font = SECONDARY_FONT
        self.sec_msg_surf = self.sec_font.render(
            'Unggoy Runner', True, '#253028')
        self.sec_msg_rect = self.sec_msg_surf.get_rect(center=(450, 190))

        self.animate_states = ['#fbfffe', '#fcffff',
                               '#eaeaea', '#e0e0e0',
                               '#d6d6d6', '#cccccc',
                               '#c2c2c2', '#b8b8b8',
                               '#aeaeae', '#a4a4a4',
                               '#aeaeae', '#b8b8b8',
                               '#c2c2c2', '#cccccc',
                               '#d6d6d6', '#e0e0e0',
                               '#eaeaea', '#fcffff',
                               '#fbfffe']
        self.animate_counter = 0
        self.action_font = SECONDARY_FONT
        self.action_msg_surf = self.action_font.render(
            'Press space to start', True, self.animate_states[self.animate_counter])
        self.action_msg_rect = self.action_msg_surf.get_rect(center=(450, 300))

        # create level from menu
        self.create_level = create_level
        # create secret level from menu
        self.create_secret_level = create_secret_level

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # start level
            self.create_level()
        if keys[pygame.K_7]:
            self.create_secret_level()

    def animate_action_msg(self):
        self.animate_counter += 0.12
        if self.animate_counter > len(self.animate_states)-1:
            self.animate_counter = 0
        self.action_msg_surf = self.action_font.render(
            'Press space to start', True, self.animate_states[int(self.animate_counter)])

    def run(self):
        self.get_input()

        self.animate_action_msg()

        # display
        self.display_surface.blit(
            self.menu_bg, self.menu_bg.get_rect(center=(422, 235)))
        self.display_surface.blit(self.main_msg_surf, self.main_msg_rect)
        self.display_surface.blit(self.sec_msg_surf, self.sec_msg_rect)
        self.display_surface.blit(self.action_msg_surf, self.action_msg_rect)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        flood_1 = FLOOD_1_IMG
        flood_2 = FLOOD_2_IMG
        self.flood_frames = [flood_1, flood_2]
        self.flood_index = 0
        self.image = self.flood_frames[self.flood_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(WIDTH, WIDTH+100), GROUND))
        self.obstacle_speed = 9

    def animation_state(self):
        self.flood_index += 0.1
        if self.flood_index >= len(self.flood_frames):
            self.flood_index = 0
        self.image = self.flood_frames[int(self.flood_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= self.obstacle_speed
        self.destroy()


class Level:
    def __init__(self, create_menu, create_secret_level):

        # screen
        self.display_surface = pygame.display.get_surface()

        # background
        self.level_bg = LEVEL_IMG
        self.ground = GROUND_IMG

        # score
        self.score = 0
        self.start_time = time()

        # create menu from level
        self.create_menu = create_menu
        # create secret level from level
        self.create_secret_level = create_secret_level

        # player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())
        self.lives_icon = GRUNT_ICON_IMG
        self.lives = 3

        # clear obstacles
        global obstacle_group
        obstacle_group.empty()
        self.hit_sound_list = collision_sound_list
        self.hit_sound_history = []

    def collision(self):
        global obstacle_group
        if pygame.sprite.spritecollide(self.player.sprite, obstacle_group, False):
            obstacle_group.empty()
            return True
        else:
            return False

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # go back to menu
            self.create_menu(False)
        if keys[pygame.K_7]:
            self.create_secret_level()

    def display_score(self):
        current_time = int(time() - self.start_time)
        score_surf = SECONDARY_FONT.render(
            f'Score: {current_time}', False, (150, 150, 150))
        score_rect = score_surf.get_rect(center=(450, 50))
        screen.blit(score_surf, score_rect)
        return current_time

    def run(self):

        if self.collision():
            self.hit_sound_history = play_random(
                self.hit_sound_list, self.hit_sound_history)
            self.lives -= 1
            if self.lives <= 0:
                self.create_menu(True)

        global obstacle_group
        self.get_input()

        # display
        self.display_surface.blit(
            self.level_bg, self.level_bg.get_rect(midbottom=(450, HEIGHT)))
        self.display_surface.blit(
            self.ground, self.ground.get_rect(center=(450, 225)))
        self.score = self.display_score()

        self.player.update()
        self.player.draw(self.display_surface)
        obstacle_group.update()
        obstacle_group.draw(self.display_surface)


class Game:
    def __init__(self):

        # audio
        self.menu_music = pygame.mixer.Sound(
            '../audio/bg_music/Mombasa_Suite.mp3')
        self.level_music = pygame.mixer.Sound('../audio/bg_music/Peril.mp3')
        self.secret_level_music = pygame.mixer.Sound(
            '../audio/bg_music/Under_Cover_of_Night.mp3')

        # menu creation
        self.menu = Menu(self.create_level, self.create_secret_level)
        self.menu_music.play(loops=-1)
        self.status = 'menu'

    def create_level(self):
        self.level = Level(self.create_menu, self.create_secret_level)
        self.status = 'level'
        self.menu_music.stop()
        self.secret_level_music.stop()
        self.level_music.play(loops=-1)

    def create_secret_level(self):
        self.level = Level(self.create_menu, self.create_secret_level)

        # level adjustment
        self.level.level_bg = SECRET_LEVEL_IMG
        self.level.ground = SECRET_GROUND_IMG

        # player adjustment
        self.level.player.sprite.player_walk = [
            SECRET_GRUNT_1_IMG, SECRET_GRUNT_2_IMG]
        self.level.player.sprite.player_jump = SECRET_GRUNT_JUMP_IMG
        self.level.player.sprite.jump_height = -22

        self.status = 'level'
        self.menu_music.stop()
        self.level_music.stop()
        # incase 7 is pressed during secret level to start a new secret level
        self.secret_level_music.stop()
        self.secret_level_music.play(loops=-1)

    def create_menu(self, died):

        # list of voice dialogue to be played when going back to main menu
        global game_over_list

        self.menu = Menu(self.create_level, self.create_secret_level)
        self.status = 'menu'
        self.level_music.stop()
        self.secret_level_music.stop()
        if died:
            play_random(game_over_list, [])
            self.death_screen()
        self.menu_music.play(loops=-1)

    def run(self):
        if self.status == 'menu':
            self.menu.run()
            return False
        elif self.status == 'level':
            self.level.run()
            return True

    def death_screen(self):
        display_surface = pygame.display.get_surface()
        menu_bg = MENU_IMG
        #display_surface.blit(menu_bg, menu_bg.get_rect(center=(422, 235)))
        msg_surf = SECONDARY_FONT.render(
            "And this is when I knew I was doomed", True, '#fbfffe')
        msg_rect = msg_surf.get_rect(center=(450, 190))
        pygame.draw.rect(display_surface, '#253028',
                         pygame.Rect(msg_rect.topleft[0]-15, msg_rect.topleft[1]-15, 400, 50))
        display_surface.blit(msg_surf, msg_rect)
        pygame.display.update()
        sleep(3)


def play_random(list, history):
    index = randint(0, len(list)-1)
    success = False

    while success == False:
        if index not in history:
            list[index].play()
            history.append(index)
            success = True
        else:
            index = randint(0, len(list)-1)

    if len(history) >= len(list):
        history.clear()
        # last played is automatically kept in history, so as to not play again
        history.append(index)
    return history


if __name__ == '__main__':

    # pygame setup
    pygame.init()

    # background music has a sample frequency of 44.1kHz, stereo sound
    pygame.mixer.init(frequency=96000, size=-16, channels=2, buffer=1024)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Unggoy Runner!')
    clock = pygame.time.Clock()

    # load assets
    FLOOD_1_IMG = pygame.image.load(
        '../graphics/flood/walk_1.png').convert_alpha()
    FLOOD_2_IMG = pygame.image.load(
        '../graphics/flood/walk_2.png').convert_alpha()
    LEVEL_IMG = pygame.image.load(
        '../graphics/background/bg_2.jpg').convert_alpha()
    SECRET_LEVEL_IMG = pygame.image.load(
        '../graphics/background/bg_3.jpg').convert_alpha()
    GROUND_IMG = pygame.image.load('../graphics/ground.png').convert_alpha()
    SECRET_GROUND_IMG = pygame.image.load(
        '../graphics/secret_ground.png').convert_alpha()
    MENU_IMG = pygame.image.load('../graphics/background/bg_1.jpg').convert()
    MAIN_FONT = pygame.font.Font('../font/Halo.ttf', 125)
    SECONDARY_FONT = pygame.font.Font('../font/Pixeltype.ttf', 35)
    GRUNT_1_IMG = pygame.image.load(
        '../graphics/grunt/walk_1.png').convert_alpha()
    GRUNT_2_IMG = pygame.image.load(
        '../graphics/grunt/walk_2.png').convert_alpha()
    GRUNT_JUMP_IMG = pygame.image.load(
        '../graphics/grunt/jump.png').convert_alpha()
    SECRET_GRUNT_1_IMG = pygame.image.load(
        '../graphics/grunt/secret_walk_1.png').convert_alpha()
    SECRET_GRUNT_2_IMG = pygame.image.load(
        '../graphics/grunt/secret_walk_2.png').convert_alpha()
    SECRET_GRUNT_JUMP_IMG = pygame.image.load(
        '../graphics/grunt/secret_jump.png').convert_alpha()
    GRUNT_ICON_IMG = pygame.image.load(
        '../graphics/grunt/icon.png').convert_alpha()
    collision_sound_list = import_audio('../audio/sound_effects/collision')
    speech_list = import_audio('../audio/sound_effects/general')
    game_over_list = import_audio('../audio/game_over')

    # timers
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1200)  # for spawning the flood

    # flood obstacles
    obstacle_group = pygame.sprite.Group()

    game = Game()
    game_active = False

    # add if playing...
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle())

        game_active = game.run()
        pygame.display.update()
        clock.tick(60)
