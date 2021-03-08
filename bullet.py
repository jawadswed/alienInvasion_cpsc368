import pygame as pg
from pygame.sprite import Sprite
from random import randint


class Bullets:
    def __init__(self, bullet_group, alien_group, barrier_group, settings, aliens, stats, sb):
        self.bullets = bullet_group
        self.alien_group = alien_group
        self.barrier_group = barrier_group
        self.settings = settings
        self.aliens = aliens
        self.stats = stats
        self.sb = sb

    def add(self, settings, screen, ship):
        self.bullets.add(Bullet(settings=settings, screen=screen, ship=ship))

    def update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        alien_collisions = pg.sprite.groupcollide(self.bullets, self.alien_group, True, False)
        if alien_collisions:
            for aliens in alien_collisions.values():
                for alien in aliens:
                    alien.dead = True
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.check_high_score(self.stats.score)
                self.sb.prep_score()

        barrier_collisions = pg.sprite.groupcollide(self.bullets, self.barrier_group, True, False)
        if barrier_collisions:
            for barriers in barrier_collisions.values():
                for barrier in barriers:
                    barrier.remove(self.barrier_group)


        if len(self.alien_group) == 0:
            self.bullets.empty()
            self.settings.increase_speed()
            self.aliens.create_fleet()
            self.stats.level += 1
            self.sb.prep_level()

    def draw(self):
        for bullet in self.bullets.sprites():
            bullet.draw()


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        # self.color = settings.bullet_color
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

class BulletFromShip(Bullet):
    """A class to manage bullets fired from the ship"""
    def __init__(self, game, x, y):
        super().__init__(game=game, x=x, y=y)
        settings = game.settings
        self.color = settings.ship_bullet_color
        self.speed_factor = -settings.bullet_speed_factor
        self.width = settings.ship_bullet_width
        self.height = settings.ship_bullet_height

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.top = y
        self.rect.centerx = x
        self.y = float(self.rect.y)
        self.speed_factor = game.settings.bullet_speed_factor
