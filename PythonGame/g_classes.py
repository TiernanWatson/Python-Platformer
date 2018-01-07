''' Tiernan Watson Arduino Coursework '''

import pygame
import serial
import g_settings

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
 
        self.width = width
        self.height = height
        self.move_speed = g_settings.PLAYER_MOVE_VEL
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
 
        self.vel_x = 0
        self.vel_y = 0

    ''' Controls movement and collisions '''
    def update(self):
        self.do_gravity()
 
        self.rect.x += self.vel_x
 
        # Stops player walking through platforms
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vel_y
        
        # Stops player falling through platforms
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        for block in block_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom
            self.vel_y = 0

        self.check_collisions_window()

    def jump(self):
        # Checks player is on a platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platforms, False)
        self.rect.y -= 2
 
        if len(platform_hit_list) > 0 or self.rect.bottom >= g_settings.SCREEN_HEIGHT:
            self.vel_y = -10

    def do_gravity(self):
        if self.vel_y == 0:
            # Stops player sticking to platforms by their head
            self.vel_y = 1 
        else:
            self.vel_y += .32
 
        if self.rect.y >= g_settings.SCREEN_HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = g_settings.SCREEN_HEIGHT - self.rect.height

    ''' Stops player going out of window '''
    def check_collisions_window(self):
        if self.rect.right > g_settings.SCREEN_WIDTH:
            self.rect.right = g_settings.SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def move(self, move_x):
        self.vel_x = move_x * self.move_speed

 
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
 
class Level:
    def __init__(self, player, platforms, end_flag):
        self.platforms = pygame.sprite.Group()
        self.player = player
        self.end_flag = end_flag
        for p in platforms:
            block = Platform(p[0], p[1], p[2], p[3], p[4])
            block.player = self.player
            self.platforms.add(block)
 
    def draw(self, screen, light_level):
        screen.fill(light_level)
        self.platforms.draw(screen)
 

class Game_Serial:
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate = 9600, timeout = 1)
        # Fixes issue with jumbled data at the start of game
        for n in range(0, 80, 1):
            self.serial_line = self.ser.readline().decode('ascii')

    def read(self):
        self.serial_line = self.ser.readline().decode('ascii')

    def get_move_x(self):
        # [0] is right button state, [1] is left
        return int(self.serial_line[0]) - int(self.serial_line[1])

    def get_move_y(self):
        # [2] is up button state
        return int(self.serial_line[2])

    def get_light(self):
        # Returns strength 0-1 of light for multiplying in game
        return int(self.serial_line[3]) / g_settings.MAX_LIGHT
