import curses
import time
import random
random_next_time = random.randint(3, 6)

def window_setup():
    window = curses.initscr()
    curses.curs_set(0)
    sh, sw = window.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100) #speed
    return w
    
def check_collision(snake, window):
    #cell_ch = window.inch(snake[0], snake[1]) & curses.A_CHARTEXT
    colors_array = [0, 67108864]
    cell_color = window.inch(snake[0], snake[1]) & curses.A_COLOR
    if cell_color in colors_array:
        return False
    return True
    
def empty_space():
    global random_next_time
    if random_next_time == 1:
        if 1 == random.randint(0, 1):
            return False
        random_next_time = random.randint(31, 94)
        return True
    random_next_time -= 1
    return False

def move(snake, key):
    head = snake[0]
    new_head = [head[0], head[1]]
    
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head)
    
def draw_snake(snake, window):
    empty_spc = empty_space()
    for i, (y, x) in enumerate(snake):
        if i == 0:
            yx = [y, x]
            if ((check_collision(yx, window) == True) and (empty_spc == False)):
                    return "END"
            else:
                window.addch(y, x, '•', curses.color_pair(1))
        elif i == 1:
            if (empty_spc == True):
                window.addch(y, x, ' ', curses.color_pair(4))
            elif (snake[2][0] == snake[1][0]) and (snake[0][0] > snake[1][0]): #lewo dół, prawo dół
                if (snake[2][1] < snake[1][1]):
                    window.addch(y, x, '┓', curses.color_pair(2))
                else:
                    window.addch(y, x, '┏', curses.color_pair(2))
            elif (snake[2][0] == snake[1][0]) and (snake[0][0] < snake[1][0]):  # prawo góra, lewo góra  
                if (snake[2][1] < snake[1][1]):
                    window.addch(y, x, '┛', curses.color_pair(2))
                else:
                    window.addch(y, x, '┗', curses.color_pair(2))
                    
            elif (snake[2][0] > snake[1][0]) and (snake[0][0] == snake[1][0]):  # góra prawo, góra lewo    
                if (snake[0][1] < snake[1][1]):
                    window.addch(y, x, '┓', curses.color_pair(2))
                else:
                    window.addch(y, x, '┏', curses.color_pair(2))
                    
            elif (snake[2][0] < snake[1][0]) and (snake[0][0] == snake[1][0]):  # dół prawo, dół lewo    
                if (snake[0][1] < snake[1][1]):
                    window.addch(y, x, '┛', curses.color_pair(2))
                else:
                    window.addch(y, x, '┗', curses.color_pair(2))

                
            elif snake[1][0] == snake[0][0]:
                window.addch(y, x, '━', curses.color_pair(2))
            elif snake[1][1] == snake[0][1]:
                window.addch(y, x, '┃', curses.color_pair(2)) #━┃┏┓┗┛
            
                



def main():
    window = window_setup()
    sh, sw = window.getmaxyx()
    snake = [
        [sh // 2, sw // 2],
        [sh // 2, sw // 2 - 1],
        [sh // 2, sw // 2 - 2]
    ]

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    key = curses.KEY_RIGHT
    while True:
        next_key = window.getch()
        key = key if next_key == -1 else next_key
       
        move(snake, key)
        tail = snake.pop()
        if draw_snake(snake, window) == "END":
            break
           
          
    time.sleep(2)
if __name__ == "__main__":
    main()