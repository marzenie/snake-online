import curses
import json
import sys
from threading import Thread
from functions.hash_str import hash_str
from functions.run_socket import run_socket
settings_file = 'settings.json'
settings = json.load(open(settings_file))


def exit():
    sys.exit(1)
if sys.platform == "win32":
    import win32api
    win32api.SetConsoleCtrlHandler(handler, True)

def draw_menu(stdscr):

    #colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    curses.curs_set(0) # remove cursor
    
    stdscr.clear()

    bi_cb_color = curses.color_pair(1) | curses.A_BOLD | curses.A_ITALIC # bold italic, cyan black
    
    # centered title
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
    
    stdscr.addstr(13, (curses.COLS - len("START")) // 2, "START")
   
    
    #instruction
    stdscr.addstr(curses.LINES - 4, 0, '⮞ Moving up or down - arrows ↑ or ↓', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 3, 0, '⮞ To confirm Enter', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 2, 0, '⮞ To switch TAB', curses.color_pair(1))
    stdscr.addstr(curses.LINES - 1, 0, '⮞ To start typing, click the right arrow', curses.color_pair(1))
    
    # generate fields with settings
    for i, option in enumerate(dane_options):
        if (option == "Password"):
            stdscr.addstr(dane_y + 2 + i, dane_x + indentation, option + ": ***")
        else:
            stdscr.addstr(dane_y + 2 + i, dane_x + indentation, option + ": " + str(settings[option.lower()]))
    
    selected_option_type = settings['type']
    selected_option_dane = 0
    selected_label_type  = 0  # 0 - "Typ", 1 - "Dane", 2 - "START"
    
    selected   = "› "
    unselected = "  "
    
    while True:
        
        if selected_label_type == 0: # Typ 
            
            for i, option in enumerate(typ_options): # deselecting/marking in type select
                if i == selected_option_type:
                    stdscr.addstr(typ_y + 2 + i, typ_x + indentation - len(selected), selected + option, curses.A_BOLD | curses.color_pair(2)) 
                    settings['type'] = i
                else:
                    stdscr.addstr(typ_y + 2 + i, typ_x + indentation - len(unselected), unselected + option, curses.A_BOLD)
                    
        elif selected_label_type == 1:  # Dane selected
            for i, option in enumerate(dane_options): # deselecting/marking in dane select
                if i == selected_option_dane:
                    stdscr.addstr(dane_y + 2 + i, dane_x + indentation - len(selected), selected + option, curses.A_BOLD | curses.color_pair(2))
                    if key == curses.KEY_RIGHT:
                        stdscr.addstr(dane_y + 2 + i, dane_x + indentation + len(selected) + len(option), " " * 30)
                        curses.echo()
                        res = stdscr.getstr(dane_y + 2 + i, dane_x + indentation + len(selected) + len(option), 30).decode('utf-8')
                        if ((option == "Password") and (res != "***")):
                            settings[option.lower()] = hash_str(res)
                        elif (res != ""):
                            settings[option.lower()] = res
                else:
                    curses.noecho()
                    stdscr.addstr(dane_y + 2 + i, dane_x + indentation - len(unselected), unselected + option, curses.A_BOLD)
        else:  # START selected
            stdscr.addstr(13, (curses.COLS - len("START") - len(selected) - 2) // 2, selected + "START", curses.A_BOLD | curses.color_pair(2))
        
        stdscr.refresh()
        key = stdscr.getch()
        
        if key == 9:  # 9 - tab change label
            if selected_label_type == 0:
                stdscr.addstr(typ_y + 2 + settings['type'], typ_x + indentation - len(unselected), unselected + typ_options[settings['type']], curses.A_BOLD | curses.color_pair(1)) 
            if selected_label_type == 1:
                for i, option in enumerate(dane_options):
                    stdscr.addstr(dane_y + 2 + i, dane_x + indentation - len(unselected), unselected + option, curses.A_BOLD)
            if selected_label_type == 2:
                stdscr.addstr(13, (curses.COLS - len("START") - len(selected) - 2) // 2, unselected + "START", curses.A_BOLD)
                
            selected_label_type = (selected_label_type + 1) % 3 # Toggle between 0 and 1 and 2
            
            
        elif key == curses.KEY_DOWN and selected_option_type < len(typ_options) - 1 and selected_label_type == 0:
            selected_option_type += 1
        elif key == curses.KEY_UP and selected_option_type > 0 and selected_label_type == 0:
            selected_option_type -= 1
            
        elif key == curses.KEY_DOWN and selected_option_dane < len(dane_options) - 1 and selected_label_type == 1:
            selected_option_dane += 1
        elif key == curses.KEY_UP and selected_option_dane > 0 and selected_label_type == 1:
            selected_option_dane -= 1
        elif key == 10 and selected_label_type == 2:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            break
        
    
        
    
            
    stdscr.refresh()
 
    
    
if __name__ == "__main__":
    curses.wrapper(draw_menu)
    thread0 = Thread(target=run_socket)
    thread0.daemon = True
    thread0.start()
    while True:
        try:
            exit_signal = input('Type "CTRL + C" anytime to stop program\n')
        except KeyboardInterrupt:
            print("\nGoodbyeee!")
            sys.exit()
            
