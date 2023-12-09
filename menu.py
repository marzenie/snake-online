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
    host_label = "Host:"
    port_label = "Port:"
    password_label = "Password:"
    
    typ_options = ["Client", "Server"]

    typ_y, dane_y, space = 6, 6, 14
    typ_x = (curses.COLS - len(typ_label) - len(dane_label) - space) // 2
    dane_x = typ_x + len(typ_label) + space

    stdscr.addstr(typ_y, typ_x, typ_label)
    stdscr.addstr(dane_y, dane_x, dane_label)
    stdscr.addstr(dane_y + 2, dane_x + 2, host_label)
    stdscr.addstr(dane_y + 3, dane_x + 2, port_label)
    stdscr.addstr(dane_y + 4, dane_x + 2, password_label)
    
    selected_option_type = 0
    selected_option_host = ""
    selected_option_port = ""
    selected_option_password = ""


    while True:
        for i, option in enumerate(typ_options):
            if i == selected_option_type:
                stdscr.addstr(typ_y + 2 + i, typ_x, "› " + option, curses.A_BOLD | curses.color_pair(2))
            else:
                stdscr.addstr(typ_y + 2 + i, typ_x, "  " + option, curses.A_BOLD)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_option_type < len(typ_options) - 1:
            selected_option_type += 1
        elif key == curses.KEY_UP and selected_option_type > 0:
            selected_option_type -= 1
        elif key in [32, 10]: # 32 - space, 10 - enter
            stdscr.addstr(9 + len(typ_options), 0, f"Typ: {typ_options[selected_option_type]}")
            
    
    stdscr.refresh()
    stdscr.getch()
    
if __name__ == "__main__":
    curses.wrapper(draw_menu)