import curses
import json

settings = json.load(open('settings.json'))
def draw_menu(stdscr):

    #colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    curses.curs_set(0) # remove cursor
    stdscr.clear()

    bi_cb_color = curses.color_pair(1) | curses.A_BOLD | curses.A_ITALIC # bold italic, cyan black
    
    #title
    stdscr.addstr(2, (curses.COLS - len(settings['title'])) // 2, settings['title'], bi_cb_color)

    #labels name
    typ_label = "Typ:"
    dane_label = "Dane:"
  
    typ_options = ["Client", "Server"]
    dane_options = ["Host", "Port", "Password"]
    """
    typ_y = Y for typ_label
    dane_y = Y for dane_label
    space = space between typ_label and dane_label
    indentation = indentation of subcolumns
    """
    typ_y, dane_y, space, indentation = 6, 6, 14, 2

    typ_x = (curses.COLS - len(typ_label) - len(dane_label) - space) // 2
    dane_x = typ_x + len(typ_label) + space

    stdscr.addstr(typ_y, typ_x, typ_label)
    stdscr.addstr(dane_y, dane_x, dane_label)
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(curses.LINES - 4, 0, '⮞ Moving up or down - arrows ↑ or ↓', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 3, 0, '⮞ To confirm Space or enter', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 2, 0, '⮞ To switch TAB', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 1, 0, '⮞ To start typing, click the right arrow', curses.color_pair(1))
    for i, option in enumerate(dane_options):
        stdscr.addstr(dane_y + 2 + i, dane_x + indentation, option + ": ")
    
    selected_option_type = settings['type']
    selected_option_dane = 0
    selected_option_password = ""
    selected_label_type = 0  # 0 - "Typ", 1 - "Dane"
    
    selected = "› "
    unselected = "  "
    test = ""
    
    while True:
        if selected_label_type == 0: # Typ 
            for i, option in enumerate(typ_options):
                if i == selected_option_type:
                    stdscr.addstr(typ_y + 2 + i, typ_x + indentation - len(selected), selected + option, curses.A_BOLD | curses.color_pair(2))
                else:
                    stdscr.addstr(typ_y + 2 + i, typ_x + indentation - len(unselected), unselected + option, curses.A_BOLD)
                    
        else:  # Dane selected
            for i, option in enumerate(dane_options):
                if i == selected_option_dane:
                    stdscr.addstr(dane_y + 2 + i, dane_x + indentation - len(selected), selected + option, curses.A_BOLD | curses.color_pair(2))
                    if key == curses.KEY_RIGHT:
                        stdscr.addstr(dane_y + 2 + i, dane_x + indentation + len(selected) + len(option), " " * 30)
                        curses.echo()
                        test = stdscr.getstr(dane_y + 2 + i, dane_x + indentation + len(selected) + len(option), 30).decode('utf-8')
                else:
                    curses.noecho()
                    stdscr.addstr(dane_y + 2 + i, dane_x + indentation - len(unselected), unselected + option, curses.A_BOLD)
                    

        stdscr.refresh()
        key = stdscr.getch()
        
        if key == 9:  # 9 - tab change label
            selected_label_type = 1 - selected_label_type  # Toggle between 0 and 1
        elif key == curses.KEY_DOWN and selected_option_type < len(typ_options) - 1 and selected_label_type == 0:
            selected_option_type += 1
        elif key == curses.KEY_UP and selected_option_type > 0 and selected_label_type == 0:
            selected_option_type -= 1
            
        elif key == curses.KEY_DOWN and selected_option_dane < len(dane_options) - 1 and selected_label_type == 1:
            selected_option_dane += 1
        elif key == curses.KEY_UP and selected_option_dane > 0 and selected_label_type == 1:
            selected_option_dane -= 1
            
            
    stdscr.refresh()
    stdscr.getch()
    
if __name__ == "__main__":
    curses.wrapper(draw_menu)