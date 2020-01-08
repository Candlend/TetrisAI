import numpy as np
import helper

grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 8, 8, 0, 0],
    [0, 0, 0, 8, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 8, 8, 0, 8, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 8, 8, 8, 8, 8, 0, 0],
    [0, 0, 0, 0, 8, 8, 8, 0, 0, 0],
    [8, 8, 8, 0, 8, 8, 8, 0, 8, 8],
    [8, 8, 0, 0, 8, 8, 8, 0, 0, 8],
    [8, 8, 8, 0, 8, 8, 8, 0, 8, 8],
    [8, 8, 0, 8, 8, 8, 8, 0, 0, 8],
])
holes = 0
rowsWithHoles = 0
holeDepth = 0

reachableIdentifier = helper.DyeingAlgorithm(grid)
for i in range(len(grid)):
    rowHasHole = False
    for j in range(len(grid[0])):
        if reachableIdentifier[i][j] == 1:
            if grid[i][j] == 0:
                rowHasHole = True
                holes += 1
                for k in range(len(grid) - 1, -1, -1):
                    if reachableIdentifier[k][j] == 0:
                        holeDepth += (i - k - 1)
                        break
    rowsWithHoles += rowHasHole

print(helper.NormalizeGrid(grid))
print(reachableIdentifier)
print(holes)
print(rowsWithHoles)
print(holeDepth)