#!/usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import random
import copy

# define the game vars
num = 4
best_score = ".best"
try:
    bf = open(best_score, "r")
    best = int(bf.read())
    bf.close()
except:
    best = 0
    bf = open(best_score, "w")
    bf.write(str(best))
    bf.close()

screen_size = (480, 650)
default_col = (250, 248, 239)
pygame.init()
icon = "2048.jpeg"
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("2048")
screen.fill(default_col)

score_font = pygame.font.SysFont("courier", 28)
num_font = pygame.font.SysFont("courier", 58)

new_button_position = (20, 145)
new_button_size = (120, 50)

undo_button_position = (355, 145)
undo_button_size = (100, 50)


def set_icon(iconname):
    icon = pygame.Surface((32, 32))
    icon_img = pygame.image.load(iconname)
    rawicon = pygame.transform.scale(icon_img, (32,32))
    for i in range(0, 32):
        for j in range(0, 32):
            icon.set_at((i, j), rawicon.get_at((i, j)))
    pygame.display.set_icon(icon)


set_icon(icon)


class NewGame(object):
    def __init__(self):
        self.data = [[0 for i in range(num)] for j in range(num)]
        self.scores = 0
        self.zero_items = []
        self.undo_list = []

    def get_score(self):
        return self.scores

    def update_best(self):
        global best
        if self.scores > best:
            best = self.scores
            with open(best_score, "w") as fb:
                fb.write(str(best))
                fb.close()

    def update_undo(self):
        if len(self.undo_list) > 5:
            self.undo_list.remove(self.undo_list[0])
        self.undo_list.append(self.data)

    def undo(self):
        if self.undo_list:
            self.data = self.undo_list.pop()
            return True
        else:
            return False

    def init_data(self):
        self.get_zero()
        if len(self.zero_items) == 16:
            self.put_num()
            self.put_num()

    def put_num(self):
        x = random.choice([2, 2, 2, 2, 4])
        self.get_zero()
        i, j = random.choice(self.zero_items)
        self.data[i][j] = x
        self.get_zero()

    def get_zero(self):
        self.zero_items = []
        for i in range(num):
            for j in range(num):
                if self.data[i][j] == 0:
                    self.zero_items.append([i,j])

    def reset(self):
        self.data = [[0 for i in range(num)] for j in range(num)]
        self.undo_list = []
        self.scores = 0
        self.init_data()
        self.get_zero()

    def check_result(self):
        if len(self.zero_items):
            return True
        else:
            for i in range(num):
                for j in range(num-1):
                    if self.data[i][j] == self.data[i][j+1]:
                        return True
            for i in range(num-1):
                for j in range(num):
                    if self.data[i][j] == self.data[i+1][j]:
                        return True
        return False

    def move(self, direction):
        tmp_data = copy.deepcopy(self.data)
        if direction in ["up", "down", "left", "right"]:
            fc = getattr(self, 'mv_'+direction)
            tmp_data = fc(tmp_data)

        if self.data != tmp_data:
            self.update_undo()
            self.data = tmp_data
            self.update_best()
            return True
        else:
            return False

    def _sum(self, line):
        _score = 0
        tmp_list = []
        if len(line) == 0:
            tmp_list = [0, 0, 0, 0]
        elif len(line) == 1:
            tmp_list = line + [0, 0, 0]
        elif len(line) == 2:
            if line[0] == line[1]:
                _score += line[0] + line[1]
                tmp_list = [line[0] + line[1], 0, 0, 0]
            else:
                tmp_list = line + [0, 0]
        elif len(line) == 3:
            if line[0] == line[1]:
                _score += line[0] + line[1]
                tmp_list = [line[0] + line[1], line[2], 0, 0]
            elif line[1] == line[2]:
                _score += line[1] + line[2]
                tmp_list = [line[0], line[1] + line[2], 0, 0]
            else:
                tmp_list = line + [0]
        else:
            if line[0] == line[1]:
                _score += line[0] + line[1]
                if line[2] == line[3]:
                    _score += line[2] + line[3]
                    tmp_list = [line[0] + line[1], line[2]+line[3], 0, 0]
                else:
                    tmp_list = [line[0] + line[1], line[2], line[3], 0]
            elif line[1] == line[2]:
                _score += line[1] + line[2]
                tmp_list = [line[0], line[1] + line[2], line[3], 0]
            elif line[2] == line[3]:
                _score += line[2] + line[3]
                tmp_list = [line[0], line[1], line[2] + line[3], 0]
            else:
                tmp_list = line

        return (_score, tmp_list)

    def mv_left(self, data):
        for i in range(4):
            tmp_line = []
            for j in range(num):
                if data[i][j]:
                    tmp_line.append(self.data[i][j])
            _score, tmp_line = self._sum(tmp_line)
            self.scores += _score
            data[i] = tmp_line

        return data

    def mv_right(self, data):
        for i in range(4):
            tmp_line = []
            for j in reversed(range(4)):
                if data[i][j]:
                    tmp_line.append(self.data[i][j])
            _score, tmp_line = self._sum(tmp_line)
            self.scores += _score
            data[i] = tmp_line[::-1]

        return data

    def mv_up(self, data):
        for i in range(4):
            tmp_line = []
            for j in range(4):
                if data[j][i]:
                    tmp_line.append(self.data[j][i])
            _score, tmp_line = self._sum(tmp_line)
            self.scores += _score
            for k in range(4):
                data[k][i] = tmp_line[k]

        return data

    def mv_down(self, data):
        for i in range(4):
            tmp_line = []
            for j in reversed(range(4)):
                if data[j][i]:
                    tmp_line.append(self.data[j][i])
            _score, tmp_line = self._sum(tmp_line)
            self.scores += _score
            tmp_line = tmp_line[::-1]
            for k in range(4):
                data[k][i] = tmp_line[k]

        return data

def draw_base():
    # draw the 2048 box
    position = (20, 20)
    size = (180,80)
    value = "2048"
    value_col = (105, 105, 105)
    value_size = 100
    pygame.draw.rect(screen, default_col, (position, size), 0)
    title_font = pygame.font.SysFont("Arial", value_size)
    title = title_font.render(value, True, value_col)
    fs = title.get_rect()
    fs.center = (110, 60)
    screen.blit(title, fs)

    # draw the score boxes
    position = (230, 20)
    size = (110, 80)
    col = (205, 201, 201)
    pygame.draw.rect(screen, col, (position, size), 0)

    value = "Score"
    value_col = (253, 245, 230)
    scores_font = pygame.font.SysFont("Arial", 30)
    ssf = scores_font.render(value, True, value_col)
    fs = ssf.get_rect()
    fs.center = (285, 45)
    screen.blit(ssf, fs)

    # draw the Best Record boxes
    position = (350, 20)
    size = (110, 80)
    pygame.draw.rect(screen, col, (position, size), 0)

    value = "Best"
    best_font = pygame.font.SysFont("Arial", 30)
    bsf = best_font.render(value, True, value_col)
    fs = bsf.get_rect()
    fs.center = (405, 45)
    screen.blit(bsf, fs)

    # draw the information area
    value = "Join the numbers and get the 2048 block!"
    value_col = (130, 130, 130)
    info_font = pygame.font.SysFont("Arial", 27)
    isf = info_font.render(value, True, value_col)
    fs = isf.get_rect()
    fs.center = (240, 130)
    screen.blit(isf, fs)

    # draw the restart button
    button_color = (255, 240, 245)

    bg_color = (220, 220, 220)
    bg_positon = (new_button_position[0]+3, new_button_position[1]+3)
    pygame.draw.rect(screen, bg_color, (bg_positon, new_button_size), 0)
    pygame.draw.rect(screen, button_color, (new_button_position, new_button_size), 0)

    value = "Restart"
    value_col = (255,127,80)
    value_size = 36
    rt_font = pygame.font.SysFont("Arial", value_size)
    rtf = rt_font.render(value, True, value_col)
    fs = rtf.get_rect()
    fs.center = (80, 170)
    screen.blit(rtf, fs)

    # draw the undo button
    bg_positon = (undo_button_position[0] + 3, undo_button_position[1] + 3)
    pygame.draw.rect(screen, bg_color, (bg_positon, undo_button_size), 0)
    pygame.draw.rect(screen, button_color, (undo_button_position, undo_button_size), 0)
    value = "Undo"
    rt_font = pygame.font.SysFont("Arial", value_size)
    udf = rt_font.render(value, True, value_col)
    fs = udf.get_rect()
    fs.center = (405, 170)
    screen.blit(udf, fs)


def get_color(v=0):
    colors = {
        0: [255, 248, 220],
        2: [255, 250, 205],
        4: [255, 228, 181],
        8: [255, 222, 173],
        16: [255, 218, 185],
        32: [255, 193, 37],
        64: [255, 165, 0],
        128: [244, 164, 96],
        256: [255, 140, 0],
        512: [255, 127, 80],
        1024: [255, 99, 71],
        2048: [255, 69, 0],
        4096: [0, 205, 102],
        8192: [60, 179, 113]
    }
    return colors[v] if v in colors else colors[0]


def game_box(v=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], score=0):
    # draw the game area
    global best
    screen.fill(default_col)
    draw_base()
    position = (20, 200)
    size = (440, 440)
    col = (205,201,201)
    gamearea = pygame.Surface(size)
    gamearea.fill(col)
    screen.blit(gamearea, position)
    block = pygame.Surface((100, 100))

    # start to draw the game boxes
    for i in range(4):
        for j in range(4):
            bv = v[j][i]  #2**(i*4+j)
            x = position[0] + (i + 1) * 8 + i * 100
            y = position[1] + (j + 1) * 8 + j * 100
            block.fill(get_color(bv))
            screen.blit(block, (x, y))
            if bv:
                if bv < 32:
                    ft = num_font.render(str(bv), True, (119, 110, 101))
                else:
                    ft = num_font.render(str(bv), True, (249, 246, 242))
                fs = ft.get_rect()
                fs.center = (x + 50, y + 50)
                screen.blit(ft, fs)
    res = score_font.render(str(score), True, default_col)
    rslt = res.get_rect()
    rslt.center = (285, 75)
    screen.blit(res, rslt)

    res = score_font.render(str(best), True, default_col)
    rslt = res.get_rect()
    rslt.center = (405, 75)
    screen.blit(res, rslt)


game = NewGame()
game.init_data()
error_flag = False
while True:
    for event in pygame.event.get():
        #print event
        if event.type == pygame.QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            p_x, p_y = pygame.mouse.get_pos()
            x, y = new_button_position
            w, h = new_button_size
            if x < p_x < x+w and y < p_y < y+h:
                error_flag = False
                game.reset()
            x, y = undo_button_position
            w, h = undo_button_size
            if x < p_x < x+w and y < p_y < y+h:
                r = game.undo()
                #print "enter undo logic"
                #print game.undo_list
                if not r:
                    # draw a error info box
                    error_flag = True
                    error_info1 = "Undo Failed!"
                    error_info2 = "Press any key to continue..."
        elif event.type == KEYDOWN:
            error_flag = False
            is_moved = False
            if event.key == K_LEFT:
                is_moved = game.move("left")
            elif event.key == K_RIGHT:
                is_moved = game.move("right")
            elif event.key == K_UP:
                is_moved = game.move("up")
            elif event.key == K_DOWN:
                is_moved = game.move("down")
            else:
                print "unknown key"
                continue
            if is_moved:
                game.put_num()

            if not game.check_result():
                error_flag = True
                error_info1 = "Game Over!"
                error_info2 = "Press 'Restart' for new game"

    game_box(v=game.data, score=game.scores)
    if error_flag:
        bg = pygame.Surface((320, 120))
        bg.fill((220, 220, 220))
        screen.blit(bg, (85,325))
        errbox = pygame.Surface((320, 120))
        errbox.fill((255, 228, 225))
        screen.blit(errbox, (80, 320))
        # error msg 1
        ib_font = pygame.font.SysFont("Arial", 60)
        ibf = ib_font.render(error_info1, True, (105, 105, 105))
        fs = ibf.get_rect()
        fs.center = (240, 365)
        screen.blit(ibf, fs)
        #error msg 2
        ib_font = pygame.font.SysFont("Arial", 30)
        ibf = ib_font.render(error_info2, True, (105, 105, 105))
        fs = ibf.get_rect()
        fs.center = (240, 410)
        screen.blit(ibf, fs)

    pygame.display.update()
