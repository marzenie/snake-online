import curses
import json

settings = json.load(open('settings.json'))
def draw_menu(stdscr):
    title = "Snake-Terminal Online"

    # Ustawianie koloru
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.clear()

    pink_color = curses.color_pair(1) | curses.A_BOLD | curses.A_ITALIC
    stdscr.addstr(2, (curses.COLS - len(settings['title'])) // 2, settings['title'], pink_color)

    typ_label = "Typ:"
    stdscr.addstr(6, 2, typ_label)


    typ_options = ["Client", "Server"]
    selected_option = 0

    while True:
        for i, option in enumerate(typ_options):
            if i == selected_option:
                stdscr.addstr(8 + i, len(typ_label) + 1, "* " + option, curses.A_BOLD | curses.color_pair(2))
            else:
                stdscr.addstr(8 + i, len(typ_label) + 1, "* " + option, curses.A_BOLD)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_option < len(typ_options) - 1:
            selected_option += 1
        elif key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(9 + len(typ_options), 0, f"You selected: {typ_options[selected_option]}")
    
    stdscr.refresh()
    stdscr.getch()
    
if __name__ == "__main__":
    curses.wrapper(draw_menu)