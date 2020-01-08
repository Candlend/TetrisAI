import numpy as np
import matrix_hash


def DyeingAlgorithm(grid):
    '''
    染色算法, reachableIdentifier中1表示联通的空地，-1表示不联通。
    需要transpose后的grid作为参数，返回一个transpose过的reachableIdentifier
    '''
    reachableIdentifier = np.zeros(grid.shape, dtype = 'int') 
    fringe = []
    for i in range(grid.shape[1]):
        if grid[0][i] == 0:
            reachableIdentifier[0][i] = 1
            fringe.append([0, i])

    while fringe != []:
        everyPoint = fringe.pop()
        towards = [[0, 1], [0, -1], [-1, 0], [1, 0]]
        for candidates in towards:
            newPoint = [everyPoint[0] + candidates[0], everyPoint[1] + candidates[1]]
            if newPoint[0] >= grid.shape[0] or newPoint[1] >= grid.shape[1] or newPoint[0] < 0 or newPoint[1] < 0:
                continue
            if reachableIdentifier[newPoint[0], newPoint[1]] == 0 and grid[newPoint[0], newPoint[1]] == 0:
                reachableIdentifier[newPoint[0], newPoint[1]] = 1
                fringe.append(newPoint)
    
    return reachableIdentifier

def NormalizeGrid(grid):
    '''
    去除grid的颜色，将grid表示为0、1，0为空1为方块
    '''
    newGrid = grid.copy()
    for i in range(len(newGrid)):
        for j in range(len(newGrid[0])):
            if newGrid[i][j] != 0:
                newGrid[i][j] = 1
    return newGrid

def GetRowTransition(grid):
    trans = 0
    for i in range(len(grid)):
        prev = -1
        print("trans:", trans)
        for j in range(len(grid[0])):
            if j != 0:
                if prev != grid[i][j]:
                    trans += 1
            prev = grid[i][j]
    return trans

def get_Tspin_struct(grid):
    grid = grid.tolist()
    Tspin_struct = [
        [
            [0,1],
            [0,0],
            [0,1]
        ],
        [
            [0,1],
            [0,0],
            [0,1],
            [1,1]
        ],
        [
            [1,1],
            [0,1],
            [0,0],
            [0,1]
        ],
        [
            [1,1],
            [0,1],
            [0,0],
            [0,1],
            [1,1]
        ],
        [
            [0,1,1],
            [0,0,1],
            [0,0,0],
            [1,0,1],
            [0,1,1]
        ],
        [
            [0,1,1],
            [0,0,1],
            [0,0,0],
            [1,0,1],
            [1,1,1]
        ],
        [
            [1,1,1],
            [0,0,1],
            [0,0,0],
            [1,0,1],
            [0,1,1]
        ],
        [
            [1,1,1],
            [0,0,1],
            [0,0,0],
            [1,0,1],
            [1,1,1]
        ]
        ,
        [
            [0,1,1],
            [1,0,1],
            [0,0,0],
            [0,0,1],
            [0,1,1]
        ],
        [
            [0,1,1],
            [1,0,1],
            [0,0,0],
            [0,0,1],
            [1,1,1]
        ],
        [
            [1,1,1],
            [1,0,1],
            [0,0,0],
            [0,0,1],
            [0,1,1]
        ],
        [
            [1,1,1],
            [1,0,1],
            [0,0,0],
            [0,0,1],
            [1,1,1]
        ]
    ]
    res = [0, 0, 0, 0]
    res[0] = matrix_hash.matrix_find_cnt(grid, Tspin_struct[0])
    res[1] = matrix_hash.matrix_find_cnt(grid, Tspin_struct[1]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[2])
    res[2] = matrix_hash.matrix_find_cnt(grid, Tspin_struct[3])
    res[3] = matrix_hash.matrix_find_cnt(grid, Tspin_struct[4]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[5]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[6]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[7]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[8]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[9]) + matrix_hash.matrix_find_cnt(grid, Tspin_struct[10])
    return res