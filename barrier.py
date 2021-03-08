import pygame as pg
from pygame.sprite import Sprite


class Barriers:
    def __init__(self, settings, screen, barrier_group, ship_height, game):
        self.settings = settings
        self.screen = screen
        self.barriers = barrier_group
        self.game = game
        self.ship_height = ship_height
        self.create_barriers()

    def create_barriers(self):
        settings, screen = self.settings, self.screen
        x_offset = self.settings.screen_width / 4
        for x in range(1, 4):
            barrier = Barrier(settings=settings, screen=screen, x=x_offset * x, y=self.settings.screen_height - self.ship_height * 2, ship_height=self.ship_height)
            self.barriers.add(barrier)
        # self.image = pg.image.load('images/barrier_0.bmp')
        # self.rect = self.image.get_rect()
        # self.screen_rect = screen.get_rect()

    def draw(self):
        for barrier in self.barriers.sprites(): barrier.draw()

class Barrier(Sprite):
    image = pg.image.load('images/Barrier-1.bmp')

    def __init__(self, settings, screen, x, y, ship_height):
        super().__init__()
        self.settings = settings
        self.screen = screen

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = x
        self.rect.centery = y

    def draw(self):
        self.screen.blit(self.image, self.rect)
