import os
import time 
import keyboard
import random
import math


HEIGHT = 26
WIDTH = 117
FPS = 60

table_horizontal = "\u2550"
table_vertical = "\u2551"
table_left_up = "\u2554"
table_left_down = "\u255a"
table_right_up = "\u2557"
table_right_down = "\u255d"
net = "\u2506"
ball = "\u25CF"

# System initialization
if os.name == 'nt':
    import msvcrt
    clear = lambda: os.system('cls')
    width = str(WIDTH + 5)
    height = str(HEIGHT + 5)
    os.system("mode con cols="+width+"lines="+height)
else:
    clear = lambda: os.system('clear')



# def draw_page():
#     page = u'\u2554' + u'\u2550' * WIDTH + u'\u2557' + "\n"
#     for y in range(HEIGHT-2):
#         if y != coords[1]:
#             page += u'\u2551' + " " * WIDTH + u'\u2551\n'
#         else:
#             page += u'\u2551' + " " * coords[0] + "x" + " " * (WIDTH - coords[0] - 1) + u'\u2551\n'
#     page += u'\u255a' + u'\u2550' * WIDTH + u'\u255d'
#     return page

def draw_table():
    table = [[" " for x in range(WIDTH)] + ["\n"] for y in range(HEIGHT)]
    table[0] = [table_horizontal if x == " " else x for x in table[0]]
    table[-1] = [table_horizontal if x == " " else x for x in table[0]]

    for sublist in table:
        sublist[0] = table_vertical
        sublist[-2] = table_vertical
        sublist[int(WIDTH/2)] = net

    table[0][0] = table_left_up
    table[-1][0] = table_left_down
    table[0][-2] = table_right_up
    table[-1][-2] = table_right_down

    return table


def put_object(table, coords, dim, body = "\u2588"):
    if len(body) == 1:
        for ix in range(dim["width"]):
            for iy in range(dim["height"]):
                table[coords[1]+iy][coords[0]+ix]= body


table = ""
mul_up = 0
mul_down = 0

player_1_keys = {"up": False, "down": False, "left": False, "right": False}
player_1_coords = [1, 10]
player_1_dimenstions = {"width": 2, "height": 5}

player_2_keys = {"up": False, "down": False, "left": False, "right": False}
player_2_coords = [114, 10]
player_2_dimenstions = {"width": 2, "height": 5}

ball_coords = [int(WIDTH/2), int(HEIGHT/2)]
ball_dimensions = {"width": 1, "height": 1}

def key_checker(key, up, down, left, right):
    key["up"] = keyboard.is_pressed(up)
    key["down"] = keyboard.is_pressed(down)
    key["left"] = keyboard.is_pressed(left)
    key["right"] = keyboard.is_pressed(right)

def move(player_dim, 
    coords, 
    key, 
    speed = 2):

    global mul_up
    global mul_down

    if key["up"] and coords[1] > 1:
        mul_up += speed
        if mul_up >= 1:
            coords[1] -= int(mul_up)
            if coords[1] < 1:
                coords[1] = 1
            mul_up = 0
        
    elif key["down"] and coords[1] + player_dim["height"] < HEIGHT - 1:
        mul_down += speed
        if mul_down >= 1:
            coords[1] += int(mul_down)
            if coords[1] >= HEIGHT - player_dim["height"] - 1:
                coords[1] = HEIGHT - player_dim["height"] - 1          
            mul_down = 0

    elif key["left"] and coords[0] > 1:
        coords[0] -= 1

    elif key["right"] and coords[0] + player_dim["width"] < WIDTH - 1:
        coords[0] += 1


a = random.uniform(0, 2*math.pi)
ball_move = [2*math.sin(a), 2*math.cos(a)]
# ball_move = [-1,0]

def ball_movement(ball_coords, ball_move):

    if ball_coords[0] + ball_move[0] > 1 and ball_coords[0] + ball_move[0] < WIDTH - 1:
        ball_coords[0] = int(ball_coords[0] + ball_move[0])
    else:
        ball_move[0] = -ball_move[0]

    if ball_coords[1] + ball_move[1] >= 1 and ball_coords[1] + ball_move[1] < HEIGHT - 1:
        ball_coords[1] = int(ball_coords[1] + ball_move[1])
    else:
        ball_move[1] = -ball_move[1]   


def collision(ball_coords, ball_move, player_coords, player_dim):

    for x in range(player_dim["width"]):
        for y in range(player_dim["height"]):
            if [ball_coords[0] + ball_move[0], ball_coords[1] + ball_move[1]] == [x + player_1_coords[0], y + player_1_coords[1]]:
                ball_move = [-ball_move[0], -ball_move[1]]



while True: 
    clear()    
    print(table)

    if keyboard.is_pressed('esc'):
        break

    key_checker(player_1_keys, 'w', 's', 'a', 'd')
    key_checker(player_2_keys, 'up', 'down', 'left', 'right')

    move(player_1_dimenstions, player_1_coords, player_1_keys)
    move(player_2_dimenstions, player_2_coords, player_2_keys)
    ball_movement(ball_coords, ball_move)

    table = draw_table()
    put_object(table, player_1_coords, player_1_dimenstions)
    put_object(table, player_2_coords, player_2_dimenstions)
    put_object(table, ball_coords, ball_dimensions, body = ball)

    table = [str(item) for sublist in table for item in sublist]
    table = "".join(table)
    time.sleep(1/FPS)

    
  