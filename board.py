from constants import WIDTH, HEIGHT


class Board:
    """Class to handle the game board."""

    def __init__(self, game):
        """Initialization method."""

        # Added 4 aditional rows to handle blocks that aren't in the board yet.
        self.blocks = [[None for _ in range(HEIGHT + 4)] for _ in range(WIDTH)]

        # Get the game object to handle levels and score.
        self.game = game

    def draw(self):
        """Method for drawing the board."""

        # Draw every block that is placed in the board.
        for row in self.blocks:
            for block in row:
                if block:
                    block.draw()

    def check_rows(self, rows):
        """Method for check if any of the given rows are full."""

        # Count how many rows are full to handle multiple line clearing.
        # Subtract it from each row to still getting the lines even after
        # moving it down.
        lines = 0
        for row in rows:
            is_full = True
            for x in range(WIDTH):
                if not self.blocks[x][row - lines]:
                    is_full = False

            # If the row is full, remove it, and increment the lines.
            if is_full:
                self.remove_row(row - lines)
                lines += 1

        if lines:
            self.game.update_score(lines)

    def remove_row(self, row):

        # Remove all the bloks in the row.
        for x in range(WIDTH):
            self.blocks[x][row] = None

        # Move down all the rows that are over the removed.
        for y in range(row + 1, HEIGHT):
            for x in range(WIDTH):
                if self.blocks[x][y]:
                    self.blocks[x][y].y -= 1
                self.blocks[x][y-1] = self.blocks[x][y]
