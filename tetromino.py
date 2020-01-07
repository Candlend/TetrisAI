class Tetromino:
    def __init__(self, tet_type):
        self.type = tet_type
        self.grid, self.pos = self.spawn_tet()
        self.length = len(self.grid)
        self.rotation = 0  # 0 is default, 1 is right, 2 is double, 3 is left
        self.ghost_pos = [0, 0]

    def spawn_tet(self):
        _tet = self.type
        if _tet == 's':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [1, 0, 0]
            ]
            _pos = [3, -2]
        elif _tet == 'z':
            grid = [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
        elif _tet == 'j':
            grid = [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
        elif _tet == 'l':
            grid = [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0]
            ]
            _pos = [3, -2]
        elif _tet == 't':
            grid = [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0]
            ]
            _pos = [3, -2]
        elif _tet == 'o':
            grid = [
                [1, 1],
                [1, 1]
            ]
            _pos = [4, -2]
        elif _tet == 'i':
            grid = [
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]
            _pos = [3, -2]
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
        elif direction == 'right':
            for y in range(length):
                for x in range(length):
                    new_grid[length - x - 1][y] = self.grid[y][x]
        elif direction == 'double':
            for y in range(length):
                self.grid[y].reverse()
                new_grid[length - y - 1] = self.grid[y]
        self.grid = [x[:] for x in new_grid]

    def set_direction(self, direction):
        if direction == 'up':
            pass
        elif direction == 'down':
            self.rotate("double")
        elif direction == 'left':
            self.rotate("left")
        elif direction == 'right':
            self.rotate("right")
