import util

class Tetromino:
    def __init__(self, tet_type):
        self.type = tet_type
        self.grid, self.pos = self.spawn_tet()
        self.length = len(self.grid)
        self.rotation = 0  # 0 is default, 1 is right, 2 is double, 3 is left
        self.ghost_pos = [0, 0]
        self.moving = util.Queue()
        self.size = 0

    def spawn_tet(self):
        _tet = self.type
        if _tet == 's':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
            _pos = [3, -2]
            self.size = 3
        elif _tet == 'z':
            grid = [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
            self.size = 3
        elif _tet == 'j':
            grid = [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
            self.size = 3
        elif _tet == 'l':
            grid = [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
            _pos = [3, -2]
            self.size = 3
        elif _tet == 't':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
            self.size = 3
        elif _tet == 'o':
            grid = [
                [1, 1],
                [1, 1]
            ]
            _pos = [4, -2]
            self.size = 2
        elif _tet == 'i':
            grid = [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
            _pos = [3, -2]
            self.size = 4
        else:
            raise Exception("Invalid tet type")
        return grid, _pos

    def rotate(self, direction):
        new_grid = [x[:] for x in self.grid]
        length = self.length

        if direction == 'left':
            for y in range(length):
                for x in range(length):
                    new_grid[x][length - y - 1] = self.grid[y][x]
            self.rotation -= 1
            if self.rotation == -1:
                self.rotation = 3
        elif direction == 'right':
            for y in range(length):
                for x in range(length):
                    new_grid[length - x - 1][y] = self.grid[y][x]
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
        elif direction == 'double':
            for y in range(length):
                self.grid[y].reverse()
                new_grid[length - y - 1] = self.grid[y]
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
            self.rotation += 1
            if self.rotation == 4:
                self.rotation = 0
        self.grid = [x[:] for x in new_grid]

    def get_pos(self):
        return self.pos[0], self.pos[1]

    def take_action(self, action, kick = None):
        # 0: go down 1 grid
        if action == 0:
            self.pos[1] += 1
            return 
        # 1: go left
        if action == 1:
            self.pos[0] -= 1
            return 
        # 2: go right
        if action == 2:
            self.pos[0] += 1
            return
        # 3: turn left
        if action == 3:
            self.rotate("left")
            if kick != None:
                self.pos[0] += kick[0]
                self.pos[1] += kick[1]
            return 
        # 4: turn right
        if action == 4:
            self.rotate("right")
            if kick != None:
                self.pos[0] += kick[0]
                self.pos[1] += kick[1]
            return 

        # 5: turn down
        if action == 5:
            self.rotate('double')
            return 
        return
