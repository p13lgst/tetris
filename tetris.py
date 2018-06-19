#!/usr/bin/python3

from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.write()

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from piece import Piece
from board import Board

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, TEXTURES, \
                      BLOCK_SIZE, SCORE_PER_LINE

Window.size = WINDOW_WIDTH, WINDOW_HEIGHT


class Menu(Screen):
    """The class to handle the game menu."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btn_jogar = MenuButton(
            text="Play!",
            pos_hint={
                'center_x': .5,
                'center_y': .4
            }
        )
        titulo = Label(
            text="TETRIS",
            font_size=190,
            pos_hint={
                'center_x': .5,
                'center_y': .8
            }
        )

        self.add_widget(titulo)
        btn_jogar.bind(on_press=self.start_game)
        self.add_widget(btn_jogar)
        # self.add_widget(MenuButton(text="Ajuda"))

    def start_game(self, btn):
        self.manager.current = 'game'
        game = self.manager.current_screen
        game.start()


class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = .3
        self.size_hint_x = 1
        self.background_normal = ""
        self.background_color = (0.1, .5, 0, 1)
        self.font_size = 70


class Game(Screen):
    """The screen that everything of the game happens."""
    loops_per_second = NumericProperty(3)
    score = NumericProperty(0)
    level = NumericProperty(0)
    lines = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(GameLabel(text="Score:", y=19))
        self.score_label = GameLabel(text='0', y=18)
        self.add_widget(self.score_label)
        self.level_label = GameLabel(text='Level: 0 ', y=15)
        self.add_widget(self.level_label)
        self.lines_label = GameLabel(text='Lines: 0', y=12)
        self.add_widget(self.lines_label)
        self.add_widget(GameLabel(text="Next:", y=8))

        # Draw the margin
        with self.canvas.before:
            Rectangle(
                pos=(0, 0),
                size=Window.size,
                texture=TEXTURES['margin']
            )

    def start(self):
        """Start the game."""
        self.setup()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.draw_next_piece()

    def stop(self):

        # Release the keyboard, and unschedule the game loop.
        self._keyboard.release()
        Clock.unschedule(self.event)

        # Go back to menu screen.
        self.manager.current = 'menu'

    def setup(self):
        """Setup the game to start."""

        # Set the loops per second.
        self.loops_per_second = 3

        # Clear the canvas
        self.canvas.after.clear()

        # Initialize the board
        self.board = Board(self)

        # Put the falling piece on the game.
        self.falling_piece = Piece(self)
        self.next_piece = self.falling_piece.next
        self.next_rotation = self.falling_piece.next_rotation

        # Store the score, level and cleaned lines.
        self.score = 0
        self.level = 0
        self.lines = 0
        self.level_lines = 0

        # Schedule the game_loop.
        self.event = Clock.schedule_interval(
            self.update, 1 / self.loops_per_second
        )

    def update(self, dt=0):
        """Function called for updating the game."""
        # Check if the piece was placed or not. If it is, put a new
        # falling_piece.
        # If it's not, it will move down every time it's updated.
        if not self.falling_piece.move_down():
            self.falling_piece.set_new()
            self.next_piece = self.falling_piece.next
            self.next_rotation = self.falling_piece.next_rotation
            self.draw_next_piece()
        self.draw()

    def update_score(self, lines):
        self.lines += lines
        self.level_lines += lines
        if self.level_lines >= 10:
            self.level += 1
            self.level_lines %= 10

        self.score += SCORE_PER_LINE[lines] * (self.level + 1)

    def _keyboard_closed(self):
        """Kivy's keyboard close callback."""
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """Handle key down"""

        # If the game is not running, don't handle any key.
        # The arrow keys will move the piece, except for the up arrow key that
        # will rotate the piece.
        if keycode[1] == 'down':
            self.update()
        elif keycode[1] == 'left':
            self.falling_piece.move_left()
        elif keycode[1] == 'right':
            self.falling_piece.move_right()
        elif keycode[1] == 'up':
            self.falling_piece.rotate()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def draw(self):

        # Clear the canvas
        self.canvas.after.clear()

        with self.canvas.after:

            self.board.draw()

            self.falling_piece.draw()

    def draw_next_piece(self):

        center_x = 4
        bottom_y = 3

        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(
                pos=(BLOCK_SIZE, BLOCK_SIZE*2),
                size=(BLOCK_SIZE*6, BLOCK_SIZE*6)
            )
            Color(1, 1, 1, 1)
            for x, y in self.next_piece['rotations'][self.next_rotation]:
                Rectangle(
                    size=(BLOCK_SIZE, BLOCK_SIZE),
                    pos=((x + center_x)*BLOCK_SIZE, (y + bottom_y)*BLOCK_SIZE),
                    texture=self.next_piece['texture']
                )

    def on_score(self, prefix, score):
        self.score_label.text = str(score)

    def on_level(self, instance, level):
        self.level_label.text = 'Level: ' + str(level)

    def on_lines(self, instance, lines):
        self.lines_label.text = 'Lines: ' + str(lines)


class GameLabel(Label):
    """Custom labels for the game."""

    def __init__(self, x=1, y=1, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = BLOCK_SIZE * 6, BLOCK_SIZE
        self.pos = x*BLOCK_SIZE, y*BLOCK_SIZE
        self.font_size = 36
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=self.size, pos=self.pos)


class TetrisApp(App):
    """Class to handle the application."""

    def build(self):
        """Method for building the application."""
        sm = ScreenManager()
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(Game(name="game"))
        return sm


if __name__ == '__main__':
    TetrisApp().run()
