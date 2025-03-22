from game.TD_grid import create_grid
from game.TD_grid import CoordCL
from game.TD_grid import CoordXY
from game.TD_grid import TILE_SIZE

def test_create_grid():
    grid = create_grid()
    assert len(grid) == 20 and len(grid[0]) == 20
    for i in range (len(grid)):
        for j in range(len(grid)):
            assert grid[i][j] == None

def test_CoordCL():
    assert CoordCL(0,0) == (0,0)
    assert CoordCL(95,540) == (3, 18)

def test_CoordXY():
    xy = CoordXY(0,19)
    assert xy[0] > TILE_SIZE * 0.45 and xy[0] < TILE_SIZE * 0.55 and xy[1] > TILE_SIZE * (19 + 0.45) and xy[1] < TILE_SIZE * (19 + 0.55)
    xy = CoordXY(5,12)
    assert xy[0] > TILE_SIZE * (5 + 0.45) and xy[0] < TILE_SIZE * (5 + 0.55) and xy[1] > TILE_SIZE * (12 + 0.45) and xy[1] < TILE_SIZE * (12 + 0.55)
    
test_create_grid()
test_CoordCL()