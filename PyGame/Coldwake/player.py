import time
import pygame
from pygame.locals import *

import level
import projectile
import orb
import platform
import surface_manager

class Player(pygame.sprite.DirtySprite):
    def __init__(self):
        super(Player, self).__init__()
        self.display = pygame.display.get_surface()

        frame_1 = pygame.image.load("data/images/player_frame1.png").convert_alpha()
        #to add more animation to character movement, simply add more frame
        #variables and include them in the frame_set list
        self.frame_set = [frame_1]
        self.current_frame = 0
        self.timer = time.clock()

        self.image = self.frame_set[self.current_frame]
        self.rect = pygame.Rect((0, 0), (self.image.get_width(), self.image.get_height()))
        self.pos_x = 0
        self.pos_y = self.display.get_height() - (100 + self.rect.height)
        self.is_jumping = False
        self.max_jump_height = 256
        self.current_jump = 0
        self.is_falling = True
        self.bullets = 50
        
    def update(self):

        if self.pos_x < 350:
            self.pos_x += 10
        
        if time.clock() >= self.timer + .05 and not self.is_jumping:
            try:
                self.current_frame += 1
                self.image = self.frame_set[self.current_frame]
            except IndexError:
                self.current_frame = 0
                self.image = self.frame_set[self.current_frame]
            self.timer = time.clock()


        if on_platform(self):
            self.is_jumping = False
            self.is_falling = False
            self.current_jump = 0
            self.dirty = 1
        if self.is_falling:
            self.pos_y += 8
            self.dirty = 1

        self.rect.topleft = (self.pos_x, self.pos_y)

    def jump(self):
        if self.current_jump <= self.max_jump_height and not self.is_falling:
            self.is_jumping = True
            self.current_frame = 0
            self.image = self.frame_set[self.current_frame]
            self.pos_y -= 10
            self.dirty = 1
            self.current_jump += 10
            if self.current_jump >= self.max_jump_height:
                self.is_falling = True

    def stop_jumping(self):
        self.jumping = False
        self.is_falling = True

    def shoot(self):
        if self.bullets > 0:
            surface_manager.add(projectile.Projectile(self))
            self.bullets -= 1

def on_platform(player):
    collidelist = pygame.sprite.spritecollide(player, surface_manager.surface_list, False)

    for item in collidelist:
        if type(item) is orb.Orb:
            continue
        if type(item) is platform.Platform or type(item) is platform.StartingPlatform:
            if (player.pos_y + player.rect.height) <= (item.pos_y + 8) and (player.pos_x + player.rect.width) >= item.pos_x:
                return True

    return False
