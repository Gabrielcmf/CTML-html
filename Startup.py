#!/usr/bin/python
# -*- coding: utf-8 -*-
#


import tcod
import os
import math
import textwrap
import shelve
import threading
import time
import subprocess
import winsound
import cProfile
import numpy as np
import tcod.event
import sys
import tkinter as tk
import pygame
import CTML
from bearlibterminal import terminal
from CTML import menu
from CTML import set_name
from CTML import msgbox





pygame.mixer.init()

sys.setrecursionlimit(10000)

pr = cProfile.Profile()

libtcod= tcod
#shadow_render = tcod.color_lerp(map[x][y].color * tcod.silver, tcod.darkest_grey,(1 - 1 / tile_distance_to(x, y, player)))


# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 52

BACKGROUND_COLOR = CTML.BACKGROUND_COLOR

# size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 43


LIMIT_FPS = 0

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
BACKGROUND_ALFA = 1.0

DEPTH = 0
MIN_SIZE = 5
FULL_ROOMS = False

FOV_ALGO = 0  # default FOV algorithm
FOV_LIGHT_WALLS = True  # light walls or not
TORCH_RADIUS = 10
lg_color = 0









CHAR_BLOCK1 = 176
CHAR_BULLET = 7


cona = tcod.console.Console(MAP_WIDTH, MAP_HEIGHT, order="F")
cona.clear(bg=(25, 0, 23), fg=(25, 0, 23))
panela = tcod.console.Console(SCREEN_WIDTH, PANEL_HEIGHT + 2, order="F")
panela.clear(fg=CTML.fg_tuple, bg=CTML.bg_tuple)
nama = 'Rodney'



def main_menu():
    global game_state, lg_color, monsters, every_item, every_trap, esp_range, root, BORDER_STYLE, e1, nama,fov_recompute

    print(CTML.shell)
    if CTML.shell != 1:

        BORDER_STYLE = 1
        esp_range = 0
        monsters = []
        every_item = []
        every_trap = []
        nama = 'Rodney'
        while not tcod.console_is_window_closed() and game_state != 'quit':

            # show the background image, at twice the regular console resolution
            color_1 = tcod.gold
            color_2 = tcod.darkest_green

            logo_color = [tcod.color_lerp(color_1, color_2, 0.0), tcod.color_lerp(color_1, color_2, 0.1),
                          tcod.color_lerp(color_1, color_2, 0.2), tcod.color_lerp(color_1, color_2, 0.3)
                , tcod.color_lerp(color_1, color_2, 0.4), tcod.color_lerp(color_1, color_2, 0.5),
                          tcod.color_lerp(color_1, color_2, 0.6),
                          tcod.color_lerp(color_1, color_2, 0.7), tcod.color_lerp(color_1, color_2, 0.8),
                          tcod.color_lerp(color_1, color_2, 0.9),
                          tcod.color_lerp(color_1, color_2, 1.0), tcod.color_lerp(color_1, color_2, 1.0),
                          tcod.color_lerp(color_1, color_2, 0.9), tcod.color_lerp(color_1, color_2, 0.8),
                          tcod.color_lerp(color_1, color_2, 0.7), tcod.color_lerp(color_1, color_2, 0.6),
                          tcod.color_lerp(color_1, color_2, 0.5), tcod.color_lerp(color_1, color_2, 0.4),
                          tcod.color_lerp(color_1, color_2, 0.3), tcod.color_lerp(color_1, color_2, 0.2),
                          tcod.color_lerp(color_1, color_2, 0.1), tcod.color_lerp(color_1, color_2, 0.0)]

            # show the game's title, and some credits!
            if lg_color > 0:

                time.sleep(1)
                tcod.console_set_default_foreground(0, logo_color[lg_color])
                lg_color -= 1

            elif lg_color <= 0:
                time.sleep(1)
                lg_color = 21
                tcod.console_set_default_foreground(0, logo_color[lg_color])

            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10, tcod.BKGND_NONE, tcod.CENTER, '')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 9, tcod.BKGND_NONE, tcod.CENTER,
                                     '____ ____ _  _ ____ ____    ____ ____    ___ _  _ ____    ')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 8, tcod.BKGND_NONE, tcod.CENTER,
                                     '|    |__| |  | |___ [__     |  | |___     |  |__| |___    ')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 7, tcod.BKGND_NONE, tcod.CENTER,
                                     '|___ |  |  \/  |___ ___]    |__| |        |  |  | |___    ')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 6, tcod.BKGND_NONE, tcod.CENTER,
                                     '       _  _ ____ ___     _    _ ____ _  _                 ')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 5, tcod.BKGND_NONE, tcod.CENTER,
                                     '       |\/| |__| |  \    |    | |    |__|                 ')
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 4, tcod.BKGND_NONE, tcod.CENTER,
                                     '       |  | |  | |__/    |___ | |___ |  |                 ')

            tcod.console_set_default_foreground(0, tcod.gold)
            tcod.console_print_ex(0, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 4, tcod.BKGND_NONE, tcod.CENTER,
                                     'By Gabriel_cmf')

            # show options and wait for the player's choice
            choice = menu('', ['New game', 'Continue game', 'High scores', 'Quit'], 24, False, None, False, False)

            if choice == 0:  # new game
                try:
                    #print(abc)
                    CTML.load_game
                except:
                    master = tk.Tk()
                    tk.Label(master, text="Name").grid(row=0)
                    e1 = tk.Entry(master)
                    e1.grid(row=0, column=1)
                    e1.delete(0, tk.END)
                    tk.Button(master, text='Show', command=set_name).grid(row=3, column=1, sticky=tk.W, pady=4)
                    tk.mainloop()
                    CTML.new_game()
                    CTML.play_game()
                else:
                    # render_all()
                    choice = menu(
                        'A save file has been detected, starting a new game will erase it, do you wish to proceed',
                        ['No', 'Yes'], 24, True, 'WARNING', tcod.red)

                    if choice == 1:
                        tcod.console_flush()
                        master = tk.Tk()
                        tk.Label(master, text="Name").grid(row=0)
                        e1 = tk.Entry(master)
                        e1.grid(row=0, column=1)
                        tk.Button(master, text='Show', command=set_name).grid(row=3, column=1, sticky=tk.W, pady=4)
                        tk.mainloop()
                        master.mainloop()

                        if nama != None:
                            CTML.new_game()
                            CTML.play_game()
                            return 'wait'
            if choice == 1:  # load last game
                try:
                    print('hello')
                    CTML.load_game
                    '''tcod.console_flush()
                    CTML.render_all()'''
                except:
                    print('no game to load')
                    msgbox('\n No saved game to load.\n', 24)
                else:
                    print('load')
                    CTML.load_game()
                    CTML.play_game()
                    return 'wait'
                    #fov_recompute = True

            if choice == 2:
                try:
                    print('ei')
                    # load_scores()
                except:
                    msgbox('\n No high scores where found.\n', 24)
                    return 'wait'

            if choice == 3:  # quit
                break


tcod.console_set_custom_font('assets/Tileset.png', tcod.FONT_LAYOUT_ASCII_INROW, 16, 64)

#tcod.console_set_custom_font('assets/Tileset3.png', tcod.FONT_LAYOUT_ASCII_INROW,tcod.FONT_TYPE_GREYSCALE)
root = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Caves of the Mad Lich', False, tcod.RENDERER_SDL2,order='F')
tcod.sys_set_fps(LIMIT_FPS)
tcod.sys_register_SDL_renderer('assets/SDL_render_metal.m')



'''if CTML.con == None:
   cona = tcod.console.Console(MAP_WIDTH, MAP_HEIGHT, order="F")
   cona.clear(bg=(25, 0, 23), fg=(25, 0, 23))
   #tcod.console_set_default_background(cona, BACKGROUND_COLOR)'''



'''if CTML.panel == None:
   panela = tcod.console.Console(SCREEN_WIDTH, PANEL_HEIGHT + 2, order="F")
   panela.clear(fg=CTML.fg_tuple, bg=CTML.bg_tuple)'''




game_state = None

main_menu()
print ('done')
