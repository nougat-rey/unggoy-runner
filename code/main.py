import pygame
from settings import *
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #player animation
        player_walk_1 = self.image = pygame.image.load('../graphics/grunt/walk_1.png').convert_alpha()
        player_walk_2 = self.image = pygame.image.load('../graphics/grunt/walk_2.png').convert_alpha()
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
            self.gravity = -21 #jump

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
        self.menu_bg = pygame.image.load('../graphics/background/bg_1.jpeg').convert()

        #menu messages
        self.main_font = pygame.font.Font('../font/Halo.ttf', 125)
        self.main_msg_surf = self.main_font.render('Halo', True, '#fbfffe')
        self.main_msg_rect = self.main_msg_surf.get_rect(center = (450, 125))

        self.sec_font = pygame.font.Font('../font/Pixeltype.ttf', 35)
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
        
        
        
class Level:
    def __init__(self, create_menu):
        
        #screen
        self.display_surface = pygame.display.get_surface()
        
        #background
        self.menu_bg = pygame.image.load('../graphics/background/bg_2.jpeg').convert_alpha()
        self.ground = pygame.image.load('../graphics/ground.png').convert_alpha()
        
        #create menu from level
        self.create_menu = create_menu

        #player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            #go back to menu
            self.create_menu()

    def run(self):
        self.get_input()
        
        #display
        self.display_surface.blit(self.menu_bg, self.menu_bg.get_rect(midbottom = (450,HEIGHT+50)))
        self.display_surface.blit(self.ground, self.ground.get_rect(center = (450, 225)))
        self.player.draw(self.display_surface)
        self.player.update()

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
    game = Game()        
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        game.run()
        pygame.display.update()
        clock.tick(60)
