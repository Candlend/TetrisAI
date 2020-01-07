import random
import util
import pygame


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

    def get_legal_actions(self, state):
        tet = state.cur_tetromino
        _tet = tet.type
        _pos = [0, 0]
        if _tet == 's':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
            _pos = [3, 0]
        elif _tet == 'z':
            grid = [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, 0]
        elif _tet == 'j':
            grid = [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, 0]
        elif _tet == 'l':
            grid = [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
            _pos = [3, 0]
        elif _tet == 't':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, 0]
        elif _tet == 'o':
            grid = [
                [1, 1],
                [1, 1]
            ]
            _pos = [4, 0]
        elif _tet == 'i':
            grid = [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
            _pos = [3, 0]
        else:
            raise Exception("Invalid tet type")
        action = Action(_tet, _pos, "up")
        return [action]

def play_auto():
    screen.fill((0, 0, 0))
    pygame.display.flip()
    frame = 0
    field = PlayField([32 * 2, 0])
    field.blit_previews()
    blit_stats_constants()
    game_intro()
    field.new_piece()
    game_start_time = time()
    agent = TetrisAgent()
    seconds = 0
    while True:
        state = field.get_state()
        action = agent.get_action(state)
        # action = Action("l", [4, 4], "left")
        field.take_action(action)
        next_state = field.get_state()
        reward = agent.get_reward(state, action, next_state)
        agent.observe_transition(state, action, next_state, reward)
        _time = time() - game_start_time
        screen.fill((0, 0, 0), (32 * 14, 64, 6 * 32, 20))
        screen.blit(helvetica_small.render(str(seconds), False, (150, 150, 150)), (32 * 14, 64))
        pygame.display.flip()
        pygame.event.pump()
        seconds += 1
        sleep(1)

