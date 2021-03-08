import pygame as pg
# from sprite_sheet import SpriteSheet
from pygame.sprite import Sprite
from timer import Timer


class Aliens:
    def __init__(self, settings, screen, alien_group, ship_height, game):
        self.settings = settings
        self.aliens = alien_group
        self.screen = screen
        self.game = game
        self.ship_height = ship_height
        self.create_fleet()

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        alien = Alien(settings=settings, screen=self.screen)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        aliens_per_row = self.aliens_per_row(settings=settings, alien_width=alien_width)
        rows_per_screen = self.rows_per_screen(settings=settings, alien_height=alien_height)

        for y in range(rows_per_screen):
            for x in range(aliens_per_row):
                alien = Alien(settings=settings, screen=screen, number=y // 2, x=alien_width * (4 + 1.5 * x), y=alien_height * (1 + y))
                self.aliens.add(alien)

    def aliens_per_row(self, settings, alien_width):
        space_x = settings.screen_width - 2 * alien_width
        return int(space_x / (2 * alien_width))

    def rows_per_screen(self, settings, alien_height): return 6
        # space_y = settings.screen_height - (alien_height) - self.ship_height
        # # space_y = settings.screen_height - (3 * alien_height) - self.ship_height
        # return int(space_y / (alien_height))
        # # return int(space_y / (2 * alien_height))

    def add(self, alien): self.aliens.add(alien)

    def remove(self, alien): self.aliens.aliens.remove(alien)

    def change_direction(self):
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): return True
        return False

    def check_aliens_bottom(self):
        r = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > r.bottom:
                return True
        return False

    def update(self):
        self.aliens.update()
        if self.check_edges(): self.change_direction()
        if self.check_aliens_bottom() or pg.sprite.spritecollideany(self.game.ship, self.aliens):
            # print("Resetting game")
            self.game.reset()
            return

        # for y in range(rows_per_screen):
        #     for x in range(aliens_per_row):
        # row = 5
        for alien in self.aliens.copy():
            alien.update()
            if alien.rect.bottom <= 0 or alien.reallydead: self.aliens.remove(alien)

    def draw(self):
        for alien in self.aliens.sprites(): alien.draw()


class Alien(Sprite):   # INHERITS from SPRITE

    images = [[pg.image.load('images/Purple_Alien-1.bmp'), pg.image.load('images/Purple_Alien-2.bmp')],
              [pg.image.load('images/Green_Alien-1.bmp'), pg.image.load('images/Green_Alien-2.bmp')],
              [pg.image.load('images/Orange_Alien-1.bmp'), pg.image.load('images/Orange_Alien-2.bmp')]]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(4)]

    timers = []
    for i in range(3):
        timers.append(
            Timer(frames=images[i], wait=700))  # creat list of Timer objects containg frames of alien animation
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    # want list of animation frames for each alien
    # sheets = ['images/Purple_Alien.png', 'images/Green_Alien.png', 'images/Orange_Alien.png']

    def __init__(self, settings, screen, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.number = number
        self.update_requests = 0
        self.dead = False
        self.reallydead = False
        self.timer_switched = False

        self.timer = Alien.timers[number]

        self.rect = self.timer.imagerect().get_rect()

        self.rect.x = self.x = x
        self.rect.y = self.y = y

        self.x = float(self.rect.x)
        self.speed = speed

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def update(self):
        if self.dead and not self.timer_switched:
            self.timer = Alien.timer_boom
            self.timer_switched = True
        elif self.dead and self.timer_switched:
            if self.timer_boom.frame_index() == len(Alien.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.timer.reset()
        delta = self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x += delta
        self.x = self.rect.x

    def draw(self):

        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)

    @staticmethod
    def run_tests():
        print(Alien.images)