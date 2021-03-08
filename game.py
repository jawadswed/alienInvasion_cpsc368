import pygame as pg
from settings import Settings
import game_functions as gf
from pygame.sprite import Group

from sprite_sheet import SpriteSheet
from barrier import Barriers
from bullet import Bullets
from ship import Ship
from alien import Aliens, Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound

import time

from vector import Vector
from quaternion import Quaternion
from matrix import Matrix


class Game:
    def __init__(self):
        pg.init()                           # initialize pygame
        self.settings = Settings()          # create an instance of Settings for this game
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        ship_image = pg.image.load('images/fighter_jet.png')
        self.ship_height = ship_image.get_rect().height
        self.hs = 0
        self.sound = Sound(bg_music="sounds/startrek_louder.wav")
        self.sound = Sound(bg_music="sounds/startrektheme.wav")
        # self.sound = Sound(bg_music="sounds/beepbeepmusic.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.barriers = self.aliens = self.stats = self.sb = self.bullets = self.ship = None
        self.restart()
        # Point label font
        self.point_label_font = pg.font.SysFont("monospace", 22)

        # Alien one and label to show on start screen
        self.alien_one = pg.image.load('images/Orange_Alien.png')
        self.alien_one = pg.transform.scale(self.alien_one, (150, 150))
        self.alien_one_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # Alien two and label to show on start screen
        self.alien_two = pg.image.load('images/Green_Alien.png')
        self.alien_two = pg.transform.scale(self.alien_two, (150, 150))
        self.alien_two_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # Alien three and label to show on start screen
        self.alien_three = pg.image.load('images/Purple_Alien.bmp')
        self.alien_three = pg.transform.scale(self.alien_three, (150, 150))
        self.alien_three_label = self.point_label_font.render("50 pts.", 1, (255, 255, 255))

        # UFO and label to show on start screen
        self.ufo = pg.image.load('images/UFO.png')
        self.ufo = pg.transform.scale(self.ufo, (150, 150))
        self.ufo_label = self.point_label_font.render("???", 1, (255, 255, 255))

    def restart(self):
        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play")
        alien_group = Group()
        bullet_group = Group()
        barrier_group = Group()

        self.aliens = Aliens(settings=self.settings, screen=self.screen, alien_group=alien_group,
                             ship_height=self.ship_height, game=self)

        self.barriers = Barriers(settings=self.settings, screen=self.screen, barrier_group=barrier_group,
                                 ship_height=self.ship_height, game=self)

        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(settings=self.settings, screen=self.screen, stats=self.stats, sound=self.sound)
        self.bullets = Bullets(bullet_group=bullet_group, alien_group=alien_group, barrier_group=barrier_group, settings=self.settings,
                               aliens=self.aliens, stats=self.stats, sb=self.sb)
        self.ship = Ship(screen=self.screen, settings=self.settings, bullets=self.bullets, sound=self.sound)
        self.settings.init_dynamic_settings()
        self.stats.high_score = self.hs
        self.sb.prep_high_score()

    def play(self):
        while True:
            gf.check_events(settings=self.settings, screen=self.screen, stats=self.stats,
                            play_button=self.play_button, ship=self.ship, bullets=self.bullets)
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self.aliens.update()

            self.screen.fill(self.settings.bg_color)
            self.ship.draw()
            self.bullets.draw()
            self.aliens.draw()
            self.barriers.draw()
            self.sb.show_score()
            if not self.stats.game_active:
                self.play_button.draw()
                self.sound.pause_bg()
            else:
                if not self.sound.playing_bg: self.sound.unpause_bg()
            pg.display.flip()

    def reset(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.aliens.empty()
            self.aliens.create_fleet()
            self.bullets.bullets.empty()
            self.ship.center_ship()
            time.sleep(0.5)
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            self.hs = self.stats.high_score
            self.restart()


def main():
    g = Game()
    g.play()
    # Vector.run_tests()
    # Quaternion.run_tests()
    # Matrix.run_tests()
    # Alien.run_tests()


if __name__ == '__main__':
    main()


# def main():
#     pg.init()
#     s = SpriteSheet('images\Purple_Alien.png')
#     r = s.makeSpriteList(93)
#
#     # Vector.run_tests()
#     # Quaternion.run_tests()
#     # Matrix.run_tests()
#     # Alien.run_tests()


if __name__ == '__main__':
        main()





























    # def sum_(*args):
    #     total = 0
    #     for el in args:
    #         total += el
    #     return total
    #
    #
    # def print_dict(**kwargs):
    #     i = 0
    #     for k, v in kwargs.items():
    #         print(f'{k}:{v}', end='')
    #         if i < len(kwargs.items()): print(', ', end='')
    #         i += 1
    #     print('\n')
    #
    #
    # def print_list_and_dict(msg, *args, **kwargs):
    #     print(f"printing '{msg}' ...")
    #     print('printing list first... ', end='')
    #     if len(args) == 0: print('list is empty', end='')
    #     for el in args:
    #         print(el, end=' ')
    #     print('\nprinting dict second... ', end='')
    #     i = 0
    #     if len(kwargs.items()) == 0: print('dictionary is empty', end='')
    #     for k, v in kwargs.items():
    #         print(f'{k}:{v}', end='')
    #         if i < len(kwargs.items()): print(', ', end='')
    #         i += 1
    #     print('\n')
    #
    #
    # def make_person(lname, fname, age, zip):
    #     person = {'lname': lname, 'fname': fname, 'age': age, 'zip': zip}
    #     return person.copy()

    # print(sum_(1, 2))
    # print(sum_(1, 2, 3))
    # print(sum_(1, 2, 3, 4))
    # print(sum_(1, 2, 3, 4, 5))
    # print(sum_(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    # print(sum_(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
    #
    # print('\n')
    # print_dict(name='Star Trek', year=2430, ship='Enterprise', captain='James T. Kirk')
    #
    # print_list_and_dict("1, 2, 3, 4, 5", 1, 2, 3, 4, 5)
    # print_list_and_dict("1, 2, 3, 4, five=5", 1, 2, 3, 4, five=5)
    # print_list_and_dict("1, 2, 3, four=4, five=5", 1, 2, 3, four=4, five=5)
    # print_list_and_dict("1, 2, three=3, four=4, five=5", 1, 2, three=3, four=4, five=5)
    # print_list_and_dict("1, two=2, three=3, four=4, five=5", 1, two=2, three=3, four=4, five=5)
    # print_list_and_dict("one=1, two=2, three=3, four=4, five=5", one=1, two=2, three=3, four=4, five=5)
    #
    # # ORDER DOESN'T MATTER if you use DICTIONARIES, but it DOES MATTER if you use LISTS
    # print_list_and_dict("ORDER DOESN'T MATTER if you use DICTIONARIES1, 2, five=5, four=4, three=3",
    #                     1, 2, five=5, four=4, three=3)

    # CANNOT PUT list (aka positional) items after dictionary (aka keyword) items
    # print_list_and_dict("WILL NOT COMPILE -- ORDER DOESN'T MATTER if you use DICTIONARIES1, 2, five=5, four=4, three=3",
    #                     1, five=5, four=4, three=3, 2)

    # guy = {'lname': 'xxx', 'fname': 'xxx', 'age': 0, 'zip': 90000}
    # joe = guy.copy()
    # joe['lname'] = 'smith';  joe['fname'] = 'joe';  joe['age'] = 23;  joe['zip'] = 60000;
    # print(joe)
    # mike = make_person('Johnson', 'Mike', 25, 70000)
    # mike['salary'] = 150000
    # print(f'{mike["fname"]} is {mike}')
