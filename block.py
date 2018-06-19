from kivy.graphics import Rectangle

from constants import BLOCK_SIZE, ORIGIN_X, ORIGIN_Y


class Block:
    """Class to handle the blocks."""
    size = (BLOCK_SIZE, BLOCK_SIZE)

    def __init__(self, x, y, texture):
        """Initialization method"""
        self.x = x
        self.y = y
        self.texture = texture

    @property
    def pos(self):
        """This defines the position where the block should be drawn."""
        return (self.x * BLOCK_SIZE + ORIGIN_X,
                self.y * BLOCK_SIZE + ORIGIN_Y)

    def draw(self):
        """Method to draw the block."""
        Rectangle(size=self.size, pos=self.pos, texture=self.texture)
