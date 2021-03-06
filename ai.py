import random
import util
import pygame
import copy
import numpy as np
import helper
import math

tetrominoes = ['s', 'z', 'j', 'l', 't', 'o', 'i', 'garbage', 'black']
test_flag = False # test or train
L4_flag = True

class Action:
    def __init__(self, tet):
        self.tet_type = tet.type
        self.pos = tet.pos
        self.rotation = tet.rotation
        self.grid = tet.grid
        self.moving = tet.moving
        self.length = tet.length

class GameState:
    def __init__(self, field):
        self.field = field
        self.grid = self.field.field
        self.total_score = self.field.total_score
        self.next_pieces = self.field.next_pieces
        self.cur_tetromino = self.field.cur_tetromino
        self.legal_actions = field.legal_actions

    def update(self):
        self.grid = self.field.field
        self.total_score = self.field.total_score
        self.next_pieces = self.field.next_pieces
        self.cur_tetromino = self.field.cur_tetromino

    def take_action(self, action):
        self.field.take_action(action)
        self.update()

    def test_rotate_right(self, tet):
        tet.rotate('right')
        kick = None

        if not self.test_array(tet):  # rotates into block - do kick stuff
            kick = self.test_srs('right', tet)
        else:
            kick = (0, 0) # pos not change

        tet.rotate('left')
        return kick

    def test_rotate_left(self, tet):
        tet.rotate('left')
        kick = None

        if not self.test_array(tet):  # rotates into block - do kick stuff
            kick = self.test_srs('left', tet)
        else:
            kick = (0, 0) # pos not change

        tet.rotate('right')
        return kick

        
    def test_array (self, tet, offset = (0,0)):
        length = tet.length
        grid = tet.grid
        coordinates = [tet.pos[0] + offset[0], tet.pos[1] + offset[1]]

        for x in range(length):
            for y in range(length):
                if grid[x][y] == 1:
                    # test for oob or overlapping blocks
                    _x = coordinates[0] + x
                    _y = coordinates[1] + y

                    if _x < 0 or _x > 9 or _y > 19:
                        return False
                    elif _y >= 0:
                        if self.grid[_x][_y] > 0:
                            return False
                    else:
                        if self.field.overflow_field[_x][_y + 20] > 0:
                            return False
        return True

    def test_srs (self, direction, tet):
        length = tet.length
        new_rotation = tet.rotation
        old_rotation = 0
        if direction == 'right':
            old_rotation = (new_rotation - 1) % 4
        elif direction == 'left':
            old_rotation = (new_rotation + 1) % 4
        elif direction == 'double':
            old_rotation = (new_rotation - 2) % 4
        tests = []

        if length == 3:  # sztlj
            if old_rotation == 0 or old_rotation == 2:
                if new_rotation == 1:  # 0>1 or 2>1
                    tests = [(-1, 0), (-1, -1), (0, +2), (-1, +2)]
                elif new_rotation == 3:  # 0>3 or 2>3
                    tests = [(+1, 0), (+1, -1), (0, +2), (+1, +2)]
            elif old_rotation == 1:  # 1>0 or 1>2
                tests = [(+1, 0), (+1, +1), (0, -2), (+1, -2)]
            elif old_rotation == 3:  # 3>2 or 3>0
                tests = [(-1, 0), (-1, +1), (0, -2), (-1, -2)]
        elif length == 4:  # i
            if (old_rotation == 0 and new_rotation == 1) or (old_rotation == 3 and new_rotation == 2):
                tests = [(-2, 0), (+1, 0), (-2, +1), (+1, -2)]  # 0>1 or 3>2
            elif (old_rotation == 1 and new_rotation == 0) or (old_rotation == 2 and new_rotation == 3):
                tests = [(+2, 0), (-1, 0), (+2, -1), (-1, +2)]  # 1>0 or 2>3
            elif (old_rotation == 1 and new_rotation == 2) or (old_rotation == 0 and new_rotation == 3):
                tests = [(-1, 0), (+2, 0), (-1, -2), (+2, +1)]  # 1>2 or 0>3
            elif (old_rotation == 2 and new_rotation == 1) or (old_rotation == 3 and new_rotation == 0):
                tests = [(+1, 0), (-2, 0), (+1, +2), (-2, -1)]  # 2>1 or 3>0
        else:  # o - will never happen. O can't spin into a placed block
            print('how you do that!')

        for test in tests:
            if self.test_array(tet, offset=test):
                return test
        return None

class TetrisAgent:
    def __init__(self, **args):
        if (test_flag):
            self.alpha = 0
            self.epsilon = 0
        else:
            if (L4_flag):
                self.alpha = 0.00000000001 ** 2
            else:
                self.alpha = 0.000001
            self.epsilon = 0

        self.discount = 0.8
        self.QValues = util.Counter()
        self.weights = util.Counter()
        weight_file = open("settings/weights.txt", "r")
        line = weight_file.readline()
        while line:
            weight = line.split()
            self.weights[weight[0]] = eval(weight[1])
            line = weight_file.readline()
        weight_file.close()

    def quit(self):
        weight_file = open("settings/weights.txt", "w")
        lines = []
        for key, value in self.weights.items():
            lines.append(key + " " + str(value) + "\n")
        weight_file.writelines(lines)
        weight_file.close()

    def get_weights(self):
        return self.weights

    def get_next_grid(self, state, action):
        field = state.field.field.copy()
        grid = action.grid
        overflow_field = state.field.overflow_field.copy()
        coordinates = action.pos
        length = len(action.grid)

        removed_lines = 0

        for y in range(length):
            for x in range(length):
                if grid[x][y] > 0:
                    if coordinates[1] + y >= 0:
                        field[coordinates[0] + x][coordinates[1] + y] = tetrominoes.index(
                            action.tet_type) + 1  # +1 because zero is blank in field
                    else:
                        overflow_field[coordinates[0] + x][coordinates[1] + y + 20] = tetrominoes.index(
                            action.tet_type) + 1

        for y in range(length):
            if 0 <= y + coordinates[1] <= 19:
                line = field[:, y + coordinates[1]]
                if 0 not in line:
                    field = np.insert(np.delete(field, y + coordinates[1], 1), 0, overflow_field[:, 19], 1)
                    overflow_field = np.insert(np.delete(overflow_field, 19, 1), 0, np.zeros(10, dtype=np.int), 1)
                    removed_lines += 1
            elif 0 > y + coordinates[1]:
                line = overflow_field[:, y + coordinates[1] + 20]
                if 0 not in line:
                    overflow_field = np.insert(np.delete(overflow_field, y + coordinates[1] + 20, 1), 0, np.zeros(10, dtype=np.int), 1)
                    removed_lines += 1

        return field, overflow_field, removed_lines


    def get_features(self, state, action):
        feats = util.Counter()

        landingHeight = 20 - action.pos[1]# Height where the last piece is added, Prevents from increasing the pile height
        # erodedPieceCells              # (Number of rows eliminated in the last move) × (Number of bricks eliminated from the last piece added), Encourages to complete rows
        rowTransitions = 0              # Number of horizontal full to empty or empty to full transitions between the cells on the board, Makes the board homogeneous
        columnTransitions = 0           # Same thing for vertical transitions
        holes = 0                       # Number of empty cells covered by at least one full cell, Prevents from making holes
        # boardWells = 0                  # Add up all W's, which w is a well and W = (1 + 2 + · · · + depth(w)), Prevents from making wells
        wellDepth = 0
        holeDepth = 0                   # Indicates how far holes are under the surface of the pile: it is the sum of the number of full cells above each hole
        rowsWithHoles = 0               # counts the number of rows having at least one hole (two holes on the same row count for only one)
        columnHeightsAvg = 0            # Average Height of the p columns of the board
        columnHeightsMax = 0            # Maximum column height
        columnDifference = 0            # Absolute difference |hp − hp+1| between adjacent columns, There are P − 1 such features where P is the board width
        # rowEliminated = 0               # Row eliminated in the move
        # blockEliminated = 0
        # tSpinStruct = 0
        combo = 0

        combo = state.field.combo
        cur_score = state.field.total_score

        (grid_origin, overflow_grid, rowEliminated) = self.get_next_grid(state, action)

        grid = helper.NormalizeGrid(grid_origin)
        # grid_origin = state.field.field
        # grid = helper.NormalizeGrid(grid_origin)

        # Get column transition
        columnTransitions = helper.GetRowTransition(grid)

        grid = np.transpose(grid)

        # get row transition
        rowTransitions = helper.GetRowTransition(grid)

        # get holes & hole depth & rows with holes
        reachableIdentifier = helper.DyeingAlgorithm(grid)

        for i in range(len(grid)):
            rowHasHole = False
            for j in range(len(grid[0])):
                if reachableIdentifier[i][j] == 1:
                    if grid[i][j] == 0:
                        rowHasHole = True
                        holes += 1
                        for k in range(len(grid)):
                            if reachableIdentifier[k][j] == 0:
                                holeDepth += (i - k)
                                break
            rowsWithHoles += rowHasHole

        # get well depth
        topHeight = 0
        bottomHeight = 0
        topFound = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not topFound:
                    if reachableIdentifier[i][j] == 1:
                        topHeight = i
                        topFound = True
                if reachableIdentifier[i][j] == 0:
                    bottomHeight = i
        wellDepth = bottomHeight - topHeight

        # get column height avg, max, difference
        columnHeightsSum = 0
        lastColumnHeight = -1
        for c in range(len(grid_origin)):
            h = 0
            for i, j in enumerate(grid_origin[c]):
                if j != 0:
                    h = 20 - i
                    break
            if lastColumnHeight == -1:
                lastColumnHeight = h
            else:
                columnDifference += abs(h - lastColumnHeight)
                lastColumnHeight = h
            if h > columnHeightsMax:
                columnHeightsMax = h
            columnHeightsSum += h
            feats["columnHeight" + str(c)] = h
        columnHeightsAvg = columnHeightsSum / len(grid)

        # # get row eliminated
        # for i in range(len(grid)):
        #     if 0 not in grid[i]:
        #         rowEliminated += 1
        # rowEliminated += 1

        # tSpinStructs = helper.get_Tspin_struct(grid)
        # print(tSpinStructs)
        # tSpinStruct = tSpinStructs[0] + tSpinStructs[1] * 4 + tSpinStructs[2] * 16 + tSpinStructs[3] * 64

        feats["landingHeight"]       = landingHeight
        feats["rowTransitions"]      = rowTransitions
        feats["columnTransitions"]   = columnTransitions
        feats["holes"]               = holes
        # feats["boardWells"]          = boardWells
        feats["wellDepth"]           = wellDepth
        feats["holeDepth"]           = holeDepth
        feats["rowsWithHoles"]       = rowsWithHoles
        feats["columnHeightsAvg"]    = columnHeightsAvg
        feats["columnHeightsMax"]    = columnHeightsMax
        feats["columnDifference"]    = columnDifference
        # feats["rowEliminated"]       = rowEliminated
        feats["combo"]               = combo
        if (L4_flag):
            feats_copy = copy.deepcopy(feats)
            for k, v in feats_copy.items():
                feats[k + "Square"] = v ** 2
                feats[k + "Cubic"] = v ** 3
                feats[k + "Quartic"] = v ** 4

        return feats

    def get_q_value(self, state, action):
        # sum_value = 0
        # feats = self.get_features(state, action)
        # for feature, value in feats.items():
        #     sum_value += self.weights[feature] * value
        # return sum_value
        return self.get_features(state, action) * self.weights


    def get_q_value(self, state, action):
        # sum_value = 0
        # feats = self.get_features(state, action)
        # for feature, value in feats.items():
        #     sum_value += self.weights[feature] * value
        # return sum_value
        return self.get_features(state, action) * self.weights

    def get_reward(self, state, action, next_state):
        return next_state.total_score - state.total_score

    def observe_transition(self, state, action, next_state, reward):
        self.update(state, action, next_state, reward)

    def update(self, state, action, next_state, reward):
        # print("reward %d" % reward)
        features = self.get_features(state, action)
        # for feature, value in features.items():
            # print(feature + " " + str(self.weights[feature]))
            # print(value)
        # print("=======")
        diff = reward + self.discount * self.get_value(next_state) - self.get_q_value(state, action)
        m = 0

        for feature, value in features.items():
            self.weights[feature] += self.alpha * diff * value
        #     m += self.weights[feature] ** 2
        # m = math.sqrt(m)
        # if m == 0:
        #     return
        # for feature, value in features.items():
        #     self.weights[feature] = self.weights[feature] / m


    def get_policy(self, state, legal_actions):
        max_value = - float("inf")
        best_action = None
        for action in legal_actions:
            value = self.get_q_value(state, action)
            if value > max_value:
                max_value = value
                best_action = action
        return best_action

    def get_value(self, state):
        legal_actions = self.get_legal_actions(state)
        action = self.get_policy(state, legal_actions)
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
                action = self.get_policy(state, legal_actions)
        return action
    # Judge if the block has collision to now grid or out of the edge.
    def is_colli(self, tetromino, state):
        x, y = tetromino.get_pos()
        if x < 0 or x >= 10:
            return True
        for i in range(tetromino.size):
            for j in range(tetromino.size):
                # print(x,y,i,j)
                if y + j < 0:
                    continue
                if tetromino.grid[i][j] > 0 and (y + j >= 20 or x + i >= 10 or x + i < 0 or state.grid[x + i][y + j] > 0):
                    return True
        return False

    def get_legal_actions(self, state):
        return state.legal_actions
