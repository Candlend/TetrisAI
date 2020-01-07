import random
import util
import pygame
import copy

class Action:
    def __init__(self, tet_type, pos, direction):
        self.tet_type = tet_type
        self.pos = pos
        self.direction = direction
        self.grid = None  # TODO


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
        self.feats = util.Counter()

    def get_weights(self):
        return self.weights

    def get_features(self, state, action):
        return self.feats

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
        pass

    def get_legal_actions(self, state):
        actions = ['up', 'down', 'left', 'right']
        tet = state.cur_tetromino
        _tet = tet.type
        _pos = None
        grid = None
        grid, _pos = tet.spawn_tet()
        q = MovingQueue()
        q.push(tet)
        res = []
        while not q.isEmpty:
            cur = q.pop()
            
        return res

class MovingQueue(util.Queue):
    # Judge two blocks if they have collision
    def is_colli(self, a, b):
        pass

    def push(self, item):
        for i in self.list:
            if self.is_colli(i, item):
                return
        tmp = None
        tmp = copy.deepcopy(item)
        self.list.insert(0, tmp)

    def copy(self, q):
        q.list = list(self.list)