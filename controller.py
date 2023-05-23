import model
import view
from view import View
from threading import Thread
from time import sleep

user_turn: model.EnumPlayerTurns = model.EnumPlayerTurns.NONE
game_is_running = True

class Control(Thread):
    def run(self):
        global user_turn
        global game_is_running
        while game_is_running:
            key = view.stdscr.getch()
            if key == 4: 
                game_is_running = False
                break
            elif key == view.curses.KEY_LEFT:
                user_turn = model.EnumPlayerTurns.LEFT
            elif key == view.curses.KEY_RIGHT:
                user_turn = model.EnumPlayerTurns.RIGHT
            elif key == ord(' '):
                user_turn = model.EnumPlayerTurns.FIRE  


def main():
    rows = model.Game.map_height + 3
    cols = model.Game.map_width + 2
    if not View.is_window_big_enough(rows + 4, cols):
        print("window is not big enough")
        return
    View.start_session(model.Game.map_height + 3, model.Game.map_width + 2)
    model.Game.get_starting_position()
    controls = Control()
    controls.start()
    global user_turn
    global game_is_running

    View.draw(model.Game.objects, model.Game.highscore, model.Game.health)

    check = 0
    score = 0
    while game_is_running:
        check = model.Game.update(user_turn)
        score = model.Game.highscore
        View.draw(model.Game.objects, score, model.Game.health)
        user_turn = model.EnumPlayerTurns.NONE
        if check != 0:
            game_is_running = False
            break
        sleep(0.05)

    controls.join()

    if check == 1:
        View.win(score)
    elif check == -1:
        View.lose(score)

    View.end_session()


if __name__ == '__main__':
    main()