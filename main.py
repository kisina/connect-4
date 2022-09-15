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

        return '\n'.join(repr) + '\n\n'


    def add_token(self, column, player):
        if column > self.columns:
            return False
        column -= 1
        token = 'o' if player == 1 else 'x'
        if self.nb_tokens[column] < self.rows:
            self.nb_tokens[column] += 1
            self.grid[self.rows-self.nb_tokens[column]][column] = token
            return 2 if self.check_winner(token) else 0
        else:
            return 1

    def check_winner(self, token):
        COLUMN_COUNT = self.columns
        ROW_COUNT = self.rows
        M = self.grid
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if M[r][c] == token and M[r][c + 1] == token and M[r][c + 2] == token and M[r][c + 3] == token:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if M[r][c] == token and M[r + 1][c] == token and M[r + 2][c] == token and M[r + 3][c] == token:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if M[r][c] == token and M[r + 1][c + 1] == token and M[r + 2][c + 2] == token and M[r + 3][c + 3] == token:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if M[r][c] == token and M[r - 1][c + 1] == token and M[r - 2][c + 2] == token and M[r - 3][c + 3] == token:
                    return True


grid = TicTacToeGrid()

print(grid)

joueur = 1
resultat = 0
while resultat < 2:
    colonne = int(input(f"Joueur {joueur} - Choisissez la colonne: "))
    resultat = grid.add_token(colonne, joueur)
    if resultat == 0:
        print(grid)
        joueur = 2 if joueur == 1 else 1


print(grid)
print(f"Le joueur {joueur} a gagné !")

