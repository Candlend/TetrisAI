import random
import util
import pygame
import copy


class Action:
    def __init__(self, tet_type, pos, rotation, grid):
        self.tet_type = tet_type
        self.pos = pos
        self.rotation = rotation
        self.grid = grid


class GameState:
    def __init__(self, field):
        self.field = field
        self.grid = self.field.field
        self.total_score = self.field.total_score
        self.next_pieces = self.field.next_pieces
        self.cur_tetromino = self.field.cur_tetromino

    def update(self):
        self.grid = self.field.field
        self.total_score = self.field.total_score
        self.next_pieces = self.field.next_pieces
        self.cur_tetromino = self.field.cur_tetromino

    def take_action(self, action):
        self.field.take_action(action)
        self.update()


class TetrisAgent:
    def __init__(self, **args):
        self.alpha = 0.5
        self.epsilon = 0.5
        self.discount = 0.5
        self.QValues = util.Counter()
        self.weights = util.Counter()

    def get_weights(self):
        return self.weights

    def get_features(self, state, action):
        feats = util.Counter()
        landingHeight = action.pos[0]   # Height where the last piece is added, Prevents from increasing the pile height
        # erodedPieceCells              # (Number of rows eliminated in the last move) × (Number of bricks eliminated from the last piece added), Encourages to complete rows
        rowTransitions = 0              # Number of horizontal full to empty or empty to full transitions between the cells on the board, Makes the board homogeneous
        columnTransitions = 0           # Same thing for vertical transitions
        Holes = 0                       # Number of empty cells covered by at least one full cell, Prevents from making holes
        # boardWells = 0                # Add up all W's, which w is a well and W = (1 + 2 + · · · + depth(w)), Prevents from making wells


        return feats

    def get_q_value(self, state, action):
        sum_value = 0
        feats = self.get_features(state, action)
        for feature, value in feats.items():
            sum_value += self.weights[feature] * value
        return sum_value

    def get_reward(self, state, action, next_state):
        return next_state.total_score - state.total_score

    def observe_transition(self, state, action, next_state, reward):
        self.update(state, action, next_state, reward)

    def update(self, state, action, next_state, reward):
        features = self.get_features(state, action)
        diff = reward + self.discount * self.get_value(next_state) - self.get_q_value(state, action)
        for feature, value in features.items():
            self.weights[feature] += self.alpha * diff * value

    def get_policy(self, state):
        max_value = - float("inf")
        best_action = None
        for action in self.get_legal_actions(state):
            value = self.get_q_value(state, action)
            if value > max_value:
                max_value = value
                best_action = action
        return best_action

    def get_value(self, state):
        action = self.get_policy(state)
        if action is None:
            return 0.0
        return self.get_q_value(state, action)

    def get_action(self, state):
        legal_actions = self.get_legal_actions(state)
        action = None
        if len(legal_actions) != 0:
            if util.flipCoin(self.epsilon):
                action = random.choice(legal_actions)
            else:
                action = self.get_policy(state)
        return action
    # Judge if the block has collision to now grid or out of the edge.
    def is_colli(self, tetromino, state):
        x, y = tetromino.get_pos()
        for i in range(tetromino.size):
            for j in range(tetromino.size):
                # print(x,y,i,j)
                if tetromino.grid[i][j] > 0 and (y + j >= 20
                 or x + i >= 10 or x + i < 0
                 or state.grid[x + i][y + j] > 0):
                    return True
        return False

    def get_legal_actions(self, state):
        actions = [0, 1, 2, 3, 4, 5]  # fall left right rl rr double
        tet = state.cur_tetromino
        _tet = tet.type
        _pos = None
        grid = None
        grid, _pos = tet.spawn_tet()
        q = util.Queue()
        close_set = [[[False for ___ in range(4)] for __ in range(25)] for _ in range(10)]
        q.push(tet)
        close_set[_pos[0]][_pos[1]][tet.rotation] = True
        res = []
        while not q.isEmpty():
            cur = q.pop()
            x, y = cur.get_pos()
            for i in range(cur.size):
                flag = False
                for j in range(cur.size):
                    if cur.grid[i][j] > 0 and (j + y + 1 >= 20 or state.grid[i + x][j + y + 1] > 0):
                        # there is brick just under the current tetromino
                        action = Action(cur.type, cur.pos, cur.rotation, cur.grid)
                        res.append(action)
                        flag = True
                        break
                if flag:
                    break

            # expend new node
            for action in actions:
                tmp = copy.deepcopy(cur)
                tmp.take_action(action)
                tmp_x, tmp_y = tmp.get_pos()
                if not self.is_colli(tmp, state) and not close_set[tmp_x][tmp_y][tmp.rotation]:
                    q.push(tmp)
                    close_set[tmp_x][tmp_y][tmp.rotation] = True
        return res
