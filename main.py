import random
import time
import pickle

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
                if i == 0:
                    self.nb_tokens.append(0)
                self.states[(j, i)] = 0

            self.grid.append(line)

    def state(self):
        return tuple(self.states.values())

    def share_of_slot_available(self):
        return self.state().count(0)/(self.rows*self.columns)


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
        """
        :param column:
        :param player:
        :return:
          - 0 if the action was accepted (without leading to a full grid or a win)
          - 1 if the column is full
          - 2 if action makes plyer win
          - 3 if the grid is full
        """
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

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if M[r][c] == token and M[r + 1][c + 1] == token and M[r + 2][c + 2] == token and M[r + 3][c + 3] == token:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if M[r][c] == token and M[r - 1][c + 1] == token and M[r - 2][c + 2] == token and M[r - 3][c + 3] == token:
                    return True


class Player:
    def __init__(self, number, epsilon=0.5, alpha=0.4, gamma=0.7, q_table_file_name="", human=False):
        self.number = number
        self.human = human
        self.q_table = {}
        self.epsilon = epsilon #probability of exploration we want to get at the end
        self.alpha = alpha  # learing rate
        self.gamma = gamma  # Discount factor
        # To store all the states and actions in an episode to update reward later
        self.states_and_actions_in_episode = []

        self.q_table_file_name = f"q_table_player_{number}.p" if q_table_file_name == "" else q_table_file_name
        try:
            self.q_table = pickle.load(open(self.q_table_file_name, "rb"))
        except:
            self.q_table = {}

    def save_q_table(self):
        pickle.dump(self.q_table, open(self.q_table_file_name, "wb"))

    def action(self, state):
        if not self.human:
            rnd = random.random()
            if rnd < self.epsilon:
                _, action = self.get_q_max(state)
                action += 1
            else:
                action = random.randint(1, 7)
        else:
            action = int(input(f"Joueur {joueur} - Choisissez la colonne: "))

        return action

    def get_q_max(self, state):
        test = [0] * 7
        try:
            test = self.q_table[state]
        except:
            self.q_table[state] = [0] * 7

        return max(test), test.index(max(test))

    def get_q(self, state, action):
        test = 0
        action -= 1
        try:
            test = self.q_table[state][action]
        except:
            self.q_table[state] = [0] * 7
        return test

    def update_q(self, state, action, new_state, reward):
        action -= 1
        firstterm = (1 - self.alpha) * self.get_q(state, action)
        _, secondterm = self.get_q_max(new_state)
        thirdterm = self.alpha * (reward + self.gamma * secondterm)
        res = firstterm + thirdterm
        self.q_table[state][action] = res
        self.states_and_actions_in_episode.append((state, action))

    def update_q_after_episode(self, revision):
        sate, action = self.states_and_actions_in_episode[-1]
        self.q_table[state][action] += revision
        sate, action = self.states_and_actions_in_episode[-2]
        self.q_table[state][action] += revision
        sate, action = self.states_and_actions_in_episode[-3]
        self.q_table[state][action] += revision
        # for sate, action in self.states_and_actions_in_episode:
        #     self.q_table[state][action] *= revision


for i in range(1000):
    start_time = time.time()
    grid = Connect4Grid()

    player1 = Player(1, q_table_file_name="test_learning.p")
    player2 = Player(2)
    player2 = Player(2, human=True, q_table_file_name="test_learning_human.p")
    # player2 = Player(2, epsilon=0, q_table_file_name="test2.p")

    is_print_required = player1.human or player2.human

    # print(grid)
    state = grid.state()
    joueur = 1
    resultat = 0
    while resultat < 2:
        print(grid) if is_print_required else None

        colonne = player1.action(state) if joueur == 1 else player2.action(state)

        state = grid.state()
        resultat = grid.add_token(colonne, joueur)
        new_state = grid.state()
        if resultat == 1:
            reward = -1
        elif resultat == 0:
            reward = 0
        elif resultat == 2:
            reward = 1
        else:
            reward = 0

        player1.update_q(state, colonne, new_state, reward) if joueur == 1 else player2.update_q(state, colonne, new_state, reward)

        # new idea : only reward the last (or the 2 to 3 last actions) if winning
        """
              - 0 if the action was accepted (without leading to a full grid or a win)
              - 1 if the column is full
              - 2 if action makes player win
              - 3 if the grid is full
        """

        if resultat == 0:
            # print(grid)
            # print(f"Grid state: {grid.state()}")
            # print(grid.share_of_slot_available())
            # time.sleep(1)
            joueur = 2 if joueur == 1 else 1


    print(grid) if is_print_required else None
    if resultat == 3:
        print("Null game")
    else:
        print(f"Game #{i} - {time.time() - start_time} seconds - Player {joueur} is the winner!, states_and_actions_in_episode: "
              f"{len(player1.states_and_actions_in_episode)} / {len(player2.states_and_actions_in_episode)}")
        if joueur == 1:
            # player1.update_q_after_episode(1+grid.share_of_slot_available())
            # player2.update_q_after_episode(1-grid.share_of_slot_available())
            player1.update_q_after_episode(0.5)
            player2.update_q_after_episode(-0.5)
        else:
            # player2.update_q_after_episode(1 + grid.share_of_slot_available())
            # player1.update_q_after_episode(1 - grid.share_of_slot_available())
            player2.update_q_after_episode(0.5)
            player1.update_q_after_episode(-0.5)

    player1.save_q_table()
    player2.save_q_table()

    time.sleep(1) if is_print_required else None
