import pygame
from settings import *
from sys import exit

class Game:
    def __init__(self):

        #general setup
        self.game_active = False

        #audio
        self.menu_bg = pygame.mixer.Sound('../audio/Mombasa_Suite.mp3')

    def run(self):
        if self.game_active:
            self.menu_bg.stop()
        else: #in main menu
            self.menu_bg.play()

if __name__ == '__main__':

    #pygame setup
    pygame.init()
    game = Game()
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
        