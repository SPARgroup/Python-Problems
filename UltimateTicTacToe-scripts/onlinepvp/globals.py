disp = None
clock = None
FPS = 60
size = (1200, 1200) #window size
title = "Ultimate TicTacToe Multiplayer v3.0"

boardsize = (600, 600)
smallsize = (boardsize[0]//3, boardsize[1]//3)
squaresize = (smallsize[0]//3, smallsize[1]//3)

inner_padding = 20
x_o_size = (squaresize[0] - inner_padding, squaresize[1] - inner_padding)

pos = [[],[],[],[],[],[],[],[],[]]
centers = [(0,0)] * 9

board_center_offset = (10,10)


class colors:
    black = (0,0,0)
    dark_purple = (42, 28, 45)
    bgColor = dark_purple
    pass