import os
import time 
import keyboard
import random
import math


HEIGHT = 40
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

def put_text(table, text, x, y):
    for ix, char in enumerate(text):
        table[y][x+ix] = char


def put_object(table, coords, dim, body = "\u2588"):
    if len(body) == 1:
        for ix in range(dim["width"]):
            for iy in range(dim["height"]):
                table[coords[1]+iy][coords[0]+ix] = body


table = ""
mul_up = 0
mul_down = 0

table_dims = [WIDTH, HEIGHT]
table_inter_dims_max = [dim - 2 for dim in table_dims]
table_inter_dims_min = [1, 1]

player_1_keys = {"up": False, "down": False, "left": False, "right": False}
player_1_dimenstions = {"width": 2, "height": 8}
player_1_coords = [-1 + int(player_1_dimenstions["width"]), int(HEIGHT/2) - int(player_1_dimenstions["height"]/2)]
player_1_body = []


player_2_keys = {"up": False, "down": False, "left": False, "right": False}
player_2_dimenstions = {"width": 2, "height": 8}
player_2_coords = [-1 + int(WIDTH) - int(player_2_dimenstions["width"]), int(HEIGHT/2) - int(player_2_dimenstions["height"]/2)]
player_2_body = []


ball_coords = [int(WIDTH/2), int(HEIGHT/2)]
ball_dimensions = {"width": 1, "height": 1}

def key_checker(key, up, down, left, right):
    key["up"] = keyboard.is_pressed(up)
    key["down"] = keyboard.is_pressed(down)
    key["left"] = keyboard.is_pressed(left)
    key["right"] = keyboard.is_pressed(right)

def move(player_dim, 
    coords, 
    body_set, 
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

    # body_set = player_body_calc(player_dim, coords, body_set)



# 12 possible ball directions - 4 for each quarter
# 1.000000     sin(0.5 x pi)
# 0.000000     cos(0.5 x pi)
# 0.923879     sin(0.375 x pi)
# 0.382683     cos(0.375 x pi)
# 0.707107     sin(0.25 x pi)
# 0.707107     cos(0.25 x pi)
# 0.382683     sin(0.125 x pi)
# 0.923879     cos(0.125 x pi)

possible_directions = []
for i in range(4, 0, -1):
    x = 0.125*math.pi*i
    possible_directions.append([round(math.sin(x), 3), round(math.cos(x), 3)])

ball_move = random.choice(possible_directions)
# ball_move = [-1,0]
str_ball_move = "ix: " + str(ball_move[0]) + " iy: " + str(ball_move[1])


ball_next_move = [0,0]
def ball_movement(ball_coords, ball_move):
    global ball_next_move
    ball_next_move[0] += ball_move[0]
    ball_next_move[1] += ball_move[1]

    if (ball_next_move[0] >= 1 or ball_next_move[0] <= -1) and ball_next_move[1] == 0:
        ball_limits_checker(ball_coords, ball_move, "x", table_inter_dims_min, table_inter_dims_max, player_1_body)
    elif (ball_next_move[1] >= 1 or ball_next_move[1] <= -1) and ball_next_move[0] == 0:
        ball_limits_checker(ball_coords, ball_move, "y", table_inter_dims_min, table_inter_dims_max, player_1_body)
    elif (ball_next_move[0] >= 1 or ball_next_move[0] <= -1) and (ball_next_move[1] >= 1 or ball_next_move[1] <= -1):
        ball_limits_checker(ball_coords, ball_move, "x", table_inter_dims_min, table_inter_dims_max, player_1_body)
        ball_limits_checker(ball_coords, ball_move, "y", table_inter_dims_min, table_inter_dims_max, player_1_body)



def ball_limits_checker(ball_coords, ball_move, axis, limit_dims_min, limit_dims_max, player_body):
    if axis == "x":
        ax = 0
    elif axis == "y":
        ax = 1

    ix = int(ball_next_move[ax])
    ball_coords[ax] += ix
    ball_next_move[ax] -= ix

    if ball_coords[ax] <= limit_dims_min[ax]:
        direction_changer(ball_coords, ball_move, ball_next_move, limit_dims_min, ax)

    elif ball_coords[ax] >= limit_dims_max[ax]:
        direction_changer(ball_coords, ball_move, ball_next_move, limit_dims_max, ax)

    elif tuple(ball_coords) in player_body:
        angle_changer(ball_coords, ball_move, ball_next_move, player_body, ax, ix)

def direction_changer(ball_coords, ball_move, ball_next_move, limit, axis_nr):
    ball_coords[axis_nr] = limit[axis_nr]
    ball_move[axis_nr] = -ball_move[axis_nr]
    ball_next_move[axis_nr] = -ball_next_move[axis_nr]

def angle_changer(ball_coords, ball_move, ball_next_move, player_body, axis_nr, step):
    ball_coords[axis_nr] = ball_coords[axis_nr] - int(step/abs(step))
    ball_next_move[axis_nr] = -ball_next_move[axis_nr]

    ball_move[axis_nr] = -ball_move[axis_nr]



def player_body_calc(player_dim, coords, player_body):
    s = [(x,y) for x in range(player_dim["width"]) for y in range(player_dim["height"])]
    player_body = [(l[0]+coords[0], l[1]+coords[1]) for l in s]
    return player_body

# def collision(ball_coords, ball_move, player_body):






str_ball_next_move = "ix: " + str(ball_next_move[0]) + " iy: " + str(ball_next_move[1])

while True: 
    clear()    
    print(table)

    if keyboard.is_pressed('esc'):
        break

    key_checker(player_1_keys, 'w', 's', 'a', 'd')
    key_checker(player_2_keys, 'up', 'down', 'left', 'right')

    move(player_1_dimenstions, player_1_coords, player_1_body, player_1_keys)
    move(player_2_dimenstions, player_2_coords, player_2_body, player_2_keys)
    player_1_body = player_body_calc(player_1_dimenstions, player_1_coords, player_1_body)
    # s = [(x,y) for x in range(player_1_dimenstions["width"]) for y in range(player_1_dimenstions["height"])]
    # player_1_body = [(l[0]+player_1_coords[0], l[1]+player_1_coords[1]) for l in s]
    ball_movement(ball_coords, ball_move)
    


    table = draw_table()
    put_object(table, player_1_coords, player_1_dimenstions)
    put_object(table, player_2_coords, player_2_dimenstions)
    put_object(table, ball_coords, ball_dimensions, body = ball)


    put_text(table, str_ball_move, 2, 5)
    put_text(table, str_ball_next_move, 2, 6)
    str_ball_move = "ix: " + str(ball_move[0]) + " iy: " + str(ball_move[1])
    # str_ball_next_move = "ix: " + str(ball_next_move[0]) + " iy: " + str(ball_next_move[1])

    table = [str(item) for sublist in table for item in sublist]
    table = "".join(table)
    time.sleep(1/FPS)


