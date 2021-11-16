def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))


from cmu_112_graphics import *
import random

def appStarted(app):
    app.rows = 9
    app.cols = app.rows
    app.board = [[(0, 0)] * app.rows for row in range(app.rows)]
    app.cellSize = 40
    app.margin = 10
    calcGradVec(app)
    perlin(app)

#i really do not understand what a gradient vector so i will do something random
#generates vector (dx, dy) of length 1
def calcGradVec(app):
    for row in range(app.rows):
        for col in range(app.cols):
            dx = random.randrange(0, 100)
            dx = float(dx/100)
            a2 = dx**2
            b2 = (1 - a2) ** 0.5
            dy = b2
            app.board[row][col] = (dx, dy)


def perlin(app, x, y):
    #for every pixel (lol), calculate distance from four points
    row, col = 
    #take dot product of each distance vector (x0 * x1) + (y0 * y1)
    #interpolate between dot products ?? wait if there are four dot products and only one result
    #linear interpolate between first two
    #linaer interpolate between last two
    #interpolate between those two values
    #linear interpolation function: 
    #from wikipedia bc i literally cannot do this anymore
    #    float sx = x - (float)x0;
    #    float sy = y - (float)y0;
    # use smoothstep function 3x^2 - 2x^3


    #how does that work
    pass

def getCellBoundsinCartesianCoords(app, canvas, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    return x0, y0, x1, y1

def drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, canvas, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill = "white")


def drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    for pX in range(0, 400):
        for pY in range(0, 400):
            #get perlin noise at that point
            #uhm. i dont know what value it will return. probably smthn between 0 and 1
            #multiply that by 255
            val = perlin(pX, pY)
            canvas.create_rectangle(pX - 1, pY - 1, pX + 1, pY + 1, color = (val, val, val))

runApp(width = 400, height = 400)
