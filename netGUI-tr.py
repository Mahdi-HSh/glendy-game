import pygame as pg
import math
import sys
import netEnv
# from tkinter import messagebox

player = 'trapper'
env = netEnv.netGlendy(player)
blocks = set()

circle_color = (0, 0, 255)
glenda_color = (0, 255, 0)
block_color = (255, 0, 0)

size = (625, 550)
circle_diameter = size[1]/11
circle_radius = circle_diameter/2
offset = circle_radius/5

def draw_board():
    y = circle_radius
    for c in range(env.n_columns):
        x = circle_radius
        if c%2!=0:
            x += circle_radius
        for r in range(env.n_rows):
            if env.board_state[c][r] == 0:
                pg.draw.circle(screen, circle_color, (x, y), circle_radius)
            elif env.board_state[c][r] == 1:
                pg.draw.circle(screen, block_color, (x, y), circle_radius)
            elif env.board_state[c][r] == 2:
                pg.draw.circle(screen, glenda_color, (x, y), circle_radius)
            x += circle_diameter+offset
        y += circle_diameter

pg.init()
screen = pg.display.set_mode(size)
screen.fill((255, 255, 255))
pg.display.set_caption("Glendy - Trapper")
draw_board()
pg.display.update()

base_stats = env.sock_init()
stats_list = base_stats.split('\n')
env.arrange_board(stats_list)
draw_board()
pg.display.update()

def get_event():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                x_axis = event.pos[0]
                y_axis = event.pos[1]
                row = math.floor(y_axis/circle_diameter)
                if row % 2 != 0:
                    if x_axis >= circle_radius:
                        column = math.floor((x_axis-circle_radius)/(circle_diameter+offset))
                    else:
                        column = None
                else:
                    if x_axis <= size[0]-circle_radius:
                        column = math.floor(x_axis/(circle_diameter+offset))
                    else:
                        column = None
                if column is not None and (row, column) not in blocks and (row, column) != env.glenda:
                    blocks.add((row, column))
                    return column, row

while not env.done:
    msg = env.sock.recv(1024).decode()
    if 'TURN' in msg:
        row, column = get_event()
    lines = msg.split('\n')
    lines.pop()
    env.server(cmds=lines, x=row, y=column)
    draw_board()
    pg.display.update()
    print('Updated.')

    '''
    how on earth i can manage pygame behaviors?
    line 80 should update screen after changes,
    but it does nothing (usually) unless i write an extra line of code after it.
    also, expect game to freeze while you're waiting for your rival,
    if the loop in get_event() finishes, game freezes immediately.
    (calling pygame.event.get is necessary.)
    random misbehaviors are expected too.
    '''