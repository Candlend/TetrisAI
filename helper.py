import numpy as np


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
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i][j] != 0:
                grid[i][j] = 1

def GetRowTransition(grid):
    trans = 0
    for i in range(grid.shape[0]):
        prev = -1
        for j in range(grid.shape[1]):
            if j != 0:
                if prev != grid[i][j]:
                    trans += 1
            prev = grid[i][j]
    return trans