''' Tiernan Watson Arduino Coursework '''

import pygame
import time
import serial.tools.list_ports
import urllib.request
import urllib.parse
import g_settings

from g_classes import Player
from g_classes import Game_Serial
from g_classes import Platform
from g_classes import Level

def find_ardui_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p[1]:
            return p[0]
    return ""
        
def submit_score(name, score):
    data = urllib.parse.urlencode({'name': name, 'score': score})
    data = data.encode('utf-8')
    request = urllib.request.Request("http://arduinotw.azurewebsites.net/submit.php")
    request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
    f = urllib.request.urlopen(request, data)
 
def main():
    input("Ensure Arduino is connected.  Press Enter to start.")
    port = find_ardui_port()
    username = input("Enter your name: ")
    
    pygame.init()
    screen = pygame.display.set_mode((g_settings.SCREEN_WIDTH, g_settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Run n Jump")

    player = Player(g_settings.PLAYER_WIDTH, g_settings.PLAYER_HEIGHT, g_settings.BLUE)
    g_serial = Game_Serial(port)

    # Format: [width, height, x, y, color]
    platforms = [[210, 40, 0, 500, g_settings.RED],
                 [210, 40, 260, 400, g_settings.RED],
                 [210, 40, 600, 300, g_settings.RED],
                 [400, 40, 0, 200, g_settings.RED]]
    end_flag = [0, 200, 100, 0] # Rectangle bounds for end trigger [x,y,x,y]
    cur_lvl = Level(player, platforms, end_flag)
    player.level = cur_lvl
 
    sprite_list = pygame.sprite.Group()

    player.rect.x = 120
    player.rect.y = g_settings.SCREEN_HEIGHT - player.rect.height
    sprite_list.add(player)

    is_play = True
    is_win = False
    start_time = time.time()

    print("Game Launched (check minimised windows)")
    ''' Main Game Loop '''
    while is_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_play = False

        g_serial.read()
        player.move(g_serial.get_move_x())
        # Will only be != 0 if jump pressed
        if g_serial.get_move_y() != 0:
            player.jump()

        sprite_list.update()
            
        # Check if player reached end flag
        if cur_lvl.end_flag[0] <= player.rect.left <= cur_lvl.end_flag[2]:
            if cur_lvl.end_flag[3] <= player.rect.bottom <= cur_lvl.end_flag[1]:
                is_win = True
                is_play = False
 
        # Multiplies by proportion to get brightness
        brightness = int(255 * g_serial.get_light())
        cur_lvl.draw(screen, (brightness,brightness,brightness))
        sprite_list.draw(screen)
        pygame.display.update()

    if(is_win):
        submit_score(username, int(time.time() - start_time))

    pygame.quit()
    quit()
 
if __name__ == "__main__":
    main()
