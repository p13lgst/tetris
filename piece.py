import random

from block import Block
from constants import WIDTH, HEIGHT, PIECES


class Piece:
    """Class to handle the falling pieces. """

    def __init__(self, game):

        # Select a random model for the piece.
        self.current_bag = random.sample(PIECES, 7)
        self.next_bag = random.sample(PIECES, 7)
        self.index = 0
        self.next = self.current_bag[self.index]
        self.next_rotation = random.randrange(len(self.next['rotations']))

        # Get the game widget for update and drawing calls, and for using the .
        self.game = game

        self.set_new()

    def set_new(self):
        # Set the initial position of the piece.
        self.center_x = WIDTH // 2
        self.bottom_y = HEIGHT

        self.current = self.next

        # Get a random initial rotation for the piece.
        self.rotation = self.next_rotation

        # Get the texture.
        self.texture = self.current['texture']

        # Get the blocks based in the model, and the initial rotation.
        self.blocks = [
            Block(x+self.center_x, y+self.bottom_y, self.texture)
            for x, y in self.current['rotations'][self.rotation]
        ]

        if self.index < len(PIECES) - 2:
            self.index += 1
        else:
            self.index = 0
            self.current_bag = self.next_bag
            self.next_bag = random.sample(PIECES, 7)

        self.next = self.current_bag[self.index]
        self.next_rotation = random.randrange(len(self.next['rotations']))


    def draw(self):
        """Method to draw the piece."""

        for block in self.blocks:

            # Only draw the block if it's already in a valid position at the
            # board.
            if block.y < HEIGHT:
                block.draw()

    def move_down(self):
        """Method for moving the piece down."""

        # Place the block if it's in the end or there is no block preventing
        # the pice to move down. If it can't move, place the piece on the Board
        # and return False to confirm the piece didn't move.
        if self.bottom_y == 0:
            self.place()
            return False
        for block in self.blocks:
            if self.game.board.blocks[block.x][block.y-1] is not None:
                self.place()
                return False

        # Move the piece down.
        self.bottom_y -= 1
        for block in self.blocks:
            block.y -= 1

        # Return True to confirm the piece moved.
        return True

    def move_left(self):
        """Method for moving the piece down."""

        # Check if there is nothing preventing the piece to move left.
        for block in self.blocks:
            if block.x == 0:
                return
            if self.game.board.blocks[block.x-1][block.y] is not None:
                return

        # Move the piece left.
        self.center_x -= 1
        for block in self.blocks:
            block.x -= 1

        # Draw everything to update the position.
        self.game.draw()

    def move_right(self):
        """Method for moving the piece down."""

        # Check if there is nothing preventing the piece to move left.
        for block in self.blocks:
            if block.x == WIDTH - 1:
                return
            if self.game.board.blocks[block.x+1][block.y] is not None:
                return

        # Move the piece right.
        self.center_x += 1
        for block in self.blocks:
            block.x += 1

        # Draw everything to update the position.
        self.game.draw()

    def rotate(self):
        """Method to rotate the piece."""

        # Set temporary rotation to be used if the piece can rotate.
        next_rotation = self.rotation + 1
        next_rotation %= len(self.current['rotations'])

        # Get temporary blocks for the new piece.
        new_blocks = [Block(x+self.center_x, y+self.bottom_y, self.texture)
                      for x, y in self.current['rotations'][self.rotation]]

        # Check if the rotation is valid.
        if self.can_rotate(new_blocks):

            # Set the rotation.
            self.rotation = next_rotation

            # Set the blocks of the piece rotated.
            self.blocks = new_blocks

            # Draw the game to update everything.
            self.game.draw()

    def can_rotate(self, new_blocks):
        """Method to check if the piece can rotate."""

        for block in new_blocks:
            if block.x < 0 or block.x >= WIDTH:
                return False
            if block.y < HEIGHT and self.game.board.blocks[block.x][block.y]:
                return False
        return True

    def place(self):
        """Place the piece on the board."""
        old_blocks = self.blocks

        # List to get the rows that the piece cover
        rows = []

        for block in old_blocks:

            # Chcek if the block it's over the board.
            if block.y >= HEIGHT:

                # Pause the game and exit the function.
                self.game.stop()
                return

            # Add the block to the rows if not added already.
            if block.y not in rows:
                rows.append(block.y)

            # Add the block to the board.
            self.game.board.blocks[block.x][block.y] = block

        # Check for full rows.
        self.game.board.check_rows(sorted(rows))
