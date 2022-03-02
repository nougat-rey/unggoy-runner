import pygame
from settings import *
from sys import exit

class MainMenu:
    def __init__(self):

        #background
        menu_bg = pygame.image.load('../graphics/background/bg_1.jpeg').convert_alpha()
        screen.blit(menu_bg, menu_bg.get_rect(center = (450,235)))

        #menu messages
        self.main_font = pygame.font.Font('../font/halo_outline.ttf', 100)
        main_msg_surf = self.main_font.render('Halo', True, '#000000')
        main_msg_rect = main_msg_surf.get_rect(center = (450, 125))
        self.display_surface = pygame.display.get_surface()
        self.display_surface.blit(main_msg_surf, main_msg_rect)

        self.sec_font = pygame.font.Font('../font/verdana.ttf', 22)
        sec_msg_surf = self.sec_font.render('Unggoy Runner', True, '#000000')
        sec_msg_rect = sec_msg_surf.get_rect(center = (450, 175))
        self.display_surface = pygame.display.get_surface()
        self.display_surface.blit(sec_msg_surf, sec_msg_rect)

class Game:
    def __init__(self, menu_bg_music):

        #general setup
        self.game_active = False

        #audio 
        self.menu_bg_music = menu_bg_music
        self.menu_bg_music.play(loops = -1)
        self.menu_music_playing = True

    def run(self):

        if self.game_active:
            self.menu_bg_music.stop()
            self.menu_music_playing = False
        else:
            if self.menu_music_playing == False:
                self.menu_bg_music.play()
                self.menu_music_playing = True
            menu = MainMenu()

if __name__ == '__main__':

    #pygame setup
    pygame.init()
    #background music has a sample frequency of 44.1kHz, stereo sound
    pygame.mixer.init(frequency = 96000, size=-16, channels=2, buffer=1024) 
    menu_bg = pygame.mixer.Sound('../audio/Mombasa_Suite.mp3')
    
    game = Game(menu_bg)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Unggoy Runner!')
    clock = pygame.time.Clock()
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            game.run()
            pygame.display.update()
            clock.tick(60)
    