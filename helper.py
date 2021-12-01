def getCellBoundsinCartesianCoords(app, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin

    return x0, y0, x1, y1

def gameMode_2DToIso(app, x, y):
    newX = (x - y)/2 - app.prevX
    newY = (x + y)/4 - app.prevY
    return newX, newY
