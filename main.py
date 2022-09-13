class Hole:
    def __init__(self):
        self.status = None

    def __str__(self):
        return self.status


class TicTacToeGrid:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.nb_tokens = []
        for i in range(rows):
            line = []
            for j in range(columns):
                line.append(' ')
                self.nb_tokens.append(0)

            self.grid.append(line)


    def __repr__(self):
        repr = []
        interline = "-" * (self.columns*3 + 9)
        repr.append(interline)

        for i in range(self.rows):
            repr.append(' | ' + ' | '.join(self.grid[i]) + ' | ')
            repr.append(interline)

        repr.append(' | ' + ' | '.join([str(i) for i in range(1, self.rows+2)]) + ' | ')

        return '\n'.join(repr)



grid = TicTacToeGrid()

print(grid)
