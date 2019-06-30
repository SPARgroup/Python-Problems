import pygame
disp = None
clock = None
FPS = 60
size = (1200, 1200) #window size
title = "Ultimate TicTacToe Multiplayer v3.0"

boardsize = (600, 600)
smallsize = (boardsize[0]//3, boardsize[1]//3)
square = (smallsize[0] // 3,smallsize[1] // 3)

inner_padding = 25 #for x_o
square_padding = 10

x_o_size = (square[0] - inner_padding,square[1] - inner_padding)
squaresize = (square[0] - square_padding,square[1] - square_padding)

pos = [[],[],[],[],[],[],[],[],[]]
centers = [(0,0)] * 9

board_center_offset = (0,0)

window_flags = pygame.FULLSCREEN

class colors:
    black = (0,0,0)
    dark_purple = (42, 28, 45)
    nice_black = (43, 42, 40)
    bgColor = nice_black
    pass