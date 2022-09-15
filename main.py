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

        repr.append(' | ' + ' | '.join([str(i) for i in range(1, self.rows+1)]) + ' | ')

        return '\n'.join(repr) + '\n\n'


    def add_token(self, column, player):
        if column > self.columns:
            return False
        column -= 1
        token = 'o' if player == 1 else 'x'
        if self.nb_tokens[column] < self.rows:
            self.nb_tokens[column] += 1
            self.grid[self.rows-self.nb_tokens[column]][column] = token
            return True
        else:
            return False


        def check_winner(self, token):
            #TODO: check http://romain.raveaux.free.fr/document/ReinforcementLearningbyQLearningConnectFourGame.html
            # Check on lines
            aligned = 0
            for i in range(self.rows):
                for j in range(self.colmuns):
                    self.grid[]                


grid = TicTacToeGrid()

print(grid)

print(grid.add_token(2, 1))
print(grid.add_token(4, 2))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(2, 1))
print(grid.add_token(5, 1))

print(grid)
