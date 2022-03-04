import pygame
from settings import *
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #player animation
        player_walk_1 = GRUNT_1_IMG
        player_walk_2 = GRUNT_2_IMG
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (160, GROUND))
        self.gravity = 0

    def animation_state(self):
        self.player_index += 0.05
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND:
            self.gravity = -22 #jump

    def apply_gravity(self):
        #applies when jumping, simulates falling 
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND:
            self.rect.bottom = GROUND

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Menu:
    def __init__(self, create_level):
        
        #screen
        self.display_surface = pygame.display.get_surface()

        #background
        self.menu_bg = MENU_IMG

        #menu messages
        self.main_font = MAIN_FONT
        self.main_msg_surf = self.main_font.render('Halo', True, '#fbfffe')
        self.main_msg_rect = self.main_msg_surf.get_rect(center = (450, 125))

        self.sec_font = SECONDARY_FONT
        self.sec_msg_surf = self.sec_font.render('Unggoy Runner', True, '#253028')
        self.sec_msg_rect = self.sec_msg_surf.get_rect(center = (450, 190))
        
        #create level from menu
        self.create_level = create_level

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #start level
            self.create_level()

    def run(self):
        self.get_input()

        #display
        self.display_surface.blit(self.menu_bg, self.menu_bg.get_rect(center = (422,235)))
        self.display_surface.blit(self.main_msg_surf, self.main_msg_rect)
        self.display_surface.blit(self.sec_msg_surf, self.sec_msg_rect)
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        flood_1 = FLOOD_1_IMG
        flood_2 = FLOOD_2_IMG
        self.flood_frames = [flood_1, flood_2]
        self.flood_index = 0
        self.image = self.flood_frames[self.flood_index]
        self.rect = self.image.get_rect(midbottom = (randint(WIDTH,WIDTH+100), GROUND))

    def animation_state(self):
        self.flood_index += 0.1
        if self.flood_index >= len(self.flood_frames): self.flood_index = 0
        self.image = self.flood_frames[int(self.flood_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 9
        self.destroy()

class Level:
    def __init__(self, create_menu):
        
        #screen
        self.display_surface = pygame.display.get_surface()
        
        #background
        self.level_bg = LEVEL_IMG
        self.ground = GROUND_IMG
        
        #create menu from level
        self.create_menu = create_menu

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        #clear obstacles
        global obstacle_group
        obstacle_group.empty()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            #go back to menu
            self.create_menu()

    def run(self):

        global obstacle_group
        self.get_input()

        #display
        self.display_surface.blit(self.level_bg, self.level_bg.get_rect(midbottom = (450,HEIGHT)))
        self.display_surface.blit(self.ground, self.ground.get_rect(center = (450, 225)))
        
        self.player.update()
        self.player.draw(self.display_surface)
        obstacle_group.update()
        obstacle_group.draw(self.display_surface)

class Game:
    def __init__(self):

        #audio 
        self.menu_music = pygame.mixer.Sound('../audio/Mombasa_Suite.mp3')
        self.level_music = pygame.mixer.Sound('../audio/Peril.mp3')

        #menu creation
        self.menu = Menu(self.create_level)
        self.menu_music.play(loops = -1)
        self.status = 'menu'

    def create_level(self):
        self.level = Level(self.create_menu)
        self.status = 'level'
        self.menu_music.stop()
        self.level_music.play(loops = -1)
    
    def create_menu(self):
        self.menu = Menu(self.create_level)
        self.status = 'menu'
        self.level_music.stop()
        self.menu_music.play(loops = -1)

    def run(self):

        if self.status == 'menu':
            self.menu.run()
        elif self.status == 'level':
            self.level.run()

if __name__ == '__main__':

    #pygame setup
    pygame.init()

    #background music has a sample frequency of 44.1kHz, stereo sound
    pygame.mixer.init(frequency = 96000, size=-16, channels=2, buffer=1024) 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Unggoy Runner!')
    clock = pygame.time.Clock()

    FLOOD_1_IMG = pygame.image.load('../graphics/flood/walk_1.png').convert_alpha()
    FLOOD_2_IMG = pygame.image.load('../graphics/flood/walk_2.png').convert_alpha()
    LEVEL_IMG = pygame.image.load('../graphics/background/bg_2.jpg').convert_alpha()
    GROUND_IMG = pygame.image.load('../graphics/ground.png').convert_alpha()
    MENU_IMG = pygame.image.load('../graphics/background/bg_1.jpg').convert()
    MAIN_FONT = pygame.font.Font('../font/Halo.ttf', 125)
    SECONDARY_FONT = pygame.font.Font('../font/Pixeltype.ttf', 35)
    GRUNT_1_IMG = pygame.image.load('../graphics/grunt/walk_1.png').convert_alpha()
    GRUNT_2_IMG = pygame.image.load('../graphics/grunt/walk_2.png').convert_alpha()

    #timers
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1200) #for spawning the flood

    #TODO: 
    #    - Need to re-pixelate grunt and flood due to resizing
    #    - Change color of ground to match background and move up a bit 

    #flood obstacles
    obstacle_group = pygame.sprite.Group()
    
    game = Game()        
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle())
            

        game.run()
        pygame.display.update()
        clock.tick(60)
