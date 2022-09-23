import random
import time

class Hole:
    def __init__(self):
        self.status = None

    def __str__(self):
        return self.status


class Connect4Grid:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.grid = []
        self.nb_tokens = []
        self.states = {}
        for i in range(rows):
            line = []
            for j in range(columns):
                line.append(' ')
                self.nb_tokens.append(0)
                self.states[(j, i)] = 0

            self.grid.append(line)

    def state(self):
        return tuple(self.states.values())

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
            self.states[(column, self.nb_tokens[column])] = player
            self.nb_tokens[column] += 1
            self.grid[self.rows-self.nb_tokens[column]][column] = token
            if self.check_winner(token):
                return 2
            else:
                return 3 if self.check_game_full() else 0
        else:
            nb_columns_full = 0
            for c in range(self.columns):
                if self.nb_tokens[c] == self.rows:
                    nb_columns_full += 1

            if nb_columns_full == self.columns:
                return 3
            else:
                return 1


    def check_game_full(self):
        nb_columns_full = 0
        for c in range(self.columns):
            if self.nb_tokens[c] == self.rows:
                nb_columns_full += 1

        if nb_columns_full == self.columns:
            return True
        else:
            return False

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



class Player():
    def __init__(self, number, epsilon=0.7, alpha=0.05, gamma=0.9):
        self.number = number
        self.Q = {}
        self.epsilon = epsilon #probability of exploration we want to get at the end
        self.alpha = alpha  # learing rate
        self.gamma = gamma  # Discount factor

    def action(self):
        rnd = random.random()
        if rnd < self.epsilon:
            action = random.randint(1, 7)
        else:
            action = random.randint(1, 7)
            #action = self.Q[state, :].argmax()
        return action

    def get_Q_max(self, state):
        #### !!! Faire une fonction pour distinguer get_Q_max de get_max_Q (là on renvoit la valeur il faudrait renvoyé l'index oiyr l'action avec : "return test.index(max(test))"
        test = [0] * 7
        try:
            test = self.Q[state]
        except:
            self.Q[state] = [0] * 7

        return max(test)

    def get_Q(self, state, action):
        test = 0
        action -= 1
        try:
            test = self.Q[state][action]
        except:
            self.Q[state] = [0] * 7
        return test

    def updateQ(self, state, action, new_state, reward):
        firstterm = (1 - self.alpha) * self.get_Q(state, action)
        secondterm = self.gamma * self.get_Q_max(new_state)
        thirdterm = self.alpha * (reward + secondterm)
        res = firstterm + thirdterm
        self.Q[state][action] = res

player1 = Player(1)
player2 = Player(2)

grid = Connect4Grid()

print(grid)

joueur = 1
resultat = 0
while resultat < 2:
    #colonne = int(input(f"Joueur {joueur} - Choisissez la colonne: "))
    colonne = player1.action()
    resultat = grid.add_token(colonne, joueur)
    if resultat == 0:
        print(grid)
        print(grid.state())
        time.sleep(1)
        joueur = 2 if joueur == 1 else 1


print(grid)
if resultat == 3:
    print("Partie nulle")
else:
    print(f"Le joueur {joueur} a gagné !")

