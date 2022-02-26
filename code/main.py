import pygame
from settings import *
from sys import exit


class Game:
    def __init__(self):

        #general setup
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Unggoy Runner!')
        self.clock = pygame.time.Clock()


    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()