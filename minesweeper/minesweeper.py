import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count < 1:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.safes.add(cell)  # Updates safes.
        self.moves_made.add(cell)  # Updates moves_made.

        # Updates all sentences with newly discovered cell.
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        # Adds new sentence on new cell.
        adding = set()
        row_low = -1
        clmn_low = -1
        row_high = 2
        clmn_high = 2
        if cell[0] == 0:
            row_low = 0
        elif cell[0] == self.height-1:
            row_high = 1
        if cell[1] == 0:
            clmn_low = 0
        elif cell[1] == self.width-1:
            clmn_high = 1
        for i in range(row_low, row_high):
            for j in range(clmn_low, clmn_high):
                neighbours = (cell[0]+i, cell[1]+j)
                if neighbours in self.mines:
                    count = count - 1
                elif neighbours not in self.mines | self.safes:
                    adding.add(neighbours)
        self.knowledge.append(Sentence(adding, count))

        changes = True
        while changes:  # Keeps looping until no new inferences can be made.
            popping = {"safe": [], "mine": [], "removing": []}
            for sentence in self.knowledge:
                if sentence.known_mines():  # If mines are known.
                    popping["mine"].append(sentence)
                    self.knowledge.remove(sentence)
                    changes = True
                elif sentence.known_safes():  # If safes are known.
                    popping["safe"].append(sentence)
                    self.knowledge.remove(sentence)
                    changes = True

            if changes:
                for sentence in popping["safe"]:
                    for safe_cell in sentence.cells:
                        if safe_cell not in self.safes:
                            self.mark_safe(safe_cell)
                for sentence in popping["mine"]:
                    for mine_cell in sentence.cells:
                        if mine_cell not in self.mines:
                            self.mark_mine(mine_cell)
                for sentence in self.knowledge:
                    if len(sentence.cells) < 1:
                        popping["removing"].append(sentence)
                for sentence in popping["removing"]:
                    self.knowledge.remove(sentence)
                changes = False

            subsets = []  # Adds new sentences with subset method.
            for one in self.knowledge:
                for two in self.knowledge:
                    if one != two and one.cells < two.cells:
                        subsets.append(Sentence(two.cells-one.cells, two.count-one.count))
            for sentence in subsets:
                self.knowledge.append(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe  # returns safe move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cell = (random.randrange(0, 8), random.randrange(0, 8))
        while cell in self.mines | self.moves_made:
            cell = (random.randrange(0, 8), random.randrange(0, 8))  # Creates a random cell.
        return cell