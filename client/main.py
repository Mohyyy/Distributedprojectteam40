import pygame as pg
from pygame_gui import UIManager, elements, UI_BUTTON_PRESSED, UI_TEXT_ENTRY_FINISHED

from GameProxy import Game
from Protocols import *


def main():
    # Initialize pygame
    pg.init()
    screen = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()

    # Initialize pygame_gui
    ui_manager = UIManager(WINDOW_SIZE)
    chat_box = elements.UITextBox(
        relative_rect=pg.Rect(
            (GAME_SIZE[0], GAME_SIZE[1] - CTB_HIGHT - ETB_HIGHT - BTN_HIGHT),
            (UI_SIZE, CTB_HIGHT),
        ),
        html_text="Welcome ASU 2D Car Racer 2023",
        manager=ui_manager,
    )
    text_entry = elements.UITextEntryLine(
        relative_rect=pg.Rect(
            (GAME_SIZE[0], GAME_SIZE[1] - BTN_HIGHT - ETB_HIGHT), (UI_SIZE, ETB_HIGHT)
        ),
        placeholder_text="Chat with Friends!",
        manager=ui_manager,
    )
    send_btn = elements.UIButton(
        relative_rect=pg.Rect(
            (GAME_SIZE[0], GAME_SIZE[1] - BTN_HIGHT), (UI_SIZE, BTN_HIGHT)
        ),
        text="send msg",
        manager=ui_manager,
    )

    # Initialize Game
    game_instance = Game()

    # Game Loop
    running = True
    movement: Movement = [0, 0]  # Direction and Angle
    while running:
        delta_time = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_UP, pg.K_w):
                    movement[0] = 1
                if event.key in (pg.K_DOWN, pg.K_s):
                    movement[0] = -1
                if event.key in (pg.K_LEFT, pg.K_d):
                    movement[1] = 1
                if event.key in (pg.K_RIGHT, pg.K_a):
                    movement[1] = -1
            if event.type == pg.KEYUP:
                if event.key in (pg.K_UP, pg.K_w, pg.K_DOWN, pg.K_s):
                    movement[0] = 0
                if event.key in (pg.K_LEFT, pg.K_d, pg.K_RIGHT, pg.K_a):
                    movement[1] = 0
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == send_btn:
                    msg_text = text_entry.get_text()
                    text_entry.set_text("")
                    chat_box.append_html_text(msg_text + "\n")
            if event.type == UI_TEXT_ENTRY_FINISHED:
                msg_text = text_entry.get_text()
                text_entry.set_text("")
                chat_box.append_html_text(msg_text + "\n")
            ui_manager.process_events(event)

        game_instance.update(screen, movement)
        ui_manager.update(delta_time)
        ui_manager.draw_ui(screen)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
