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

#very bad and incorrect implementation of perlin noise:

from cmu_112_graphics import *
import random

def appStarted(app):
    app.rows = 50
    app.cols = app.rows
    app.board = [[(0, 0)] * app.rows for row in range(app.rows)]
    app.cellSize = 5 #idk why this can never be less than 5..
    app.margin = 0
    app.perlinBoardLength = 50
    app.perlinBoard = [[0] * app.perlinBoardLength for row in range(app.perlinBoardLength)]
    app.timerDelay = 1000
    app.newPerlinBoard = [[0] * (app.perlinBoardLength* 2) for row in range(app.perlinBoardLength * 2)]
    app.newPerlinLength = app.perlinBoardLength * 2
    app.oct3PerlinBoard = [[0] * (app.perlinBoardLength//2) for row in range(app.perlinBoardLength//2)]
    app.oct3PerlinLength = app.perlinBoardLength//2
    app.oct4PerlinBoard = [[0] * (app.perlinBoardLength//5) for row in range(app.perlinBoardLength//5)]
    app.oct4PerlinLength = app.perlinBoardLength//5

    calcGradVec(app)
    fillPerlinBoard(app)
    perlinOctave2(app)
    perlinOctave3(app)
    perlinOctave4(app)

def timerFired(app):
    # movePerlin(app)
    pass

#generates vector (dx, dy) of length 1
def calcGradVec(app):
    for row in range(app.rows):
        for col in range(app.cols):
            dx = random.randrange(-100, 100)
            dx = float(dx/100)
            a2 = dx**2
            b2 = (1 - a2) ** 0.5
            dy = b2
            chance = random.randint(0, 1)
            if (chance == 1):
                app.board[row][col] = (dx, dy)
            else:
                app.board[row][col] = (dy, dx)

def calcDotProduct(corner, cur):
    a, b = corner
    c, d, = cur
    return (a * c + b * d)


def interpolate(a, b, t):
    return a + t *(b  - a)

def normalize(vec):
    if (vec == (0,0)):
        return vec
    x, y = vec
    length = (x**2 + y**2) ** 0.5
    return (x/length, y / length)

def perlin(app, x, y):
    #for every pixel, calculate distance from four points
    #REMINDER: COL IS X, ROW IS Y
    col = int((x - app.margin)//app.cellSize) 
    row = int((y - app.margin)//app.cellSize) 
    cornerVectorTL = app.board[row][col]
    #Turn (x, y) into decimal points
    x = float(x/app.cellSize)
    y = float(y/app.cellSize)
    distanceTL = (x - col, y - row)
    #Calculate corner gradient vectors and distance from (x, y)
    if (col + 1 < app.cols):
        cornerVectorTR = app.board[row][col + 1]
        distanceTR = (x - col - 1, y - row)
    else:
        cornerVectorTR = cornerVectorTL
        distanceTR = distanceTL
    
    if (row + 1 < app.rows):
        cornerVectorBL = app.board[row + 1][col]
        distanceBL = (x - col, y - row - 1)

    else:
        cornerVectorBL = cornerVectorTL
        distanceBL = distanceTL

    
    if (row + 1 < app.rows and col + 1 < app.cols):
        cornerVectorBR = app.board[row + 1][col + 1]
        distanceBR = (x - col - 1, y - row - 1)

    else:
        cornerVectorBR = cornerVectorTL
        distanceBR = distanceTL

    # distanceTL= normalize(distanceTL)
    # distanceTR= normalize(distanceTR)
    # distanceBL= normalize(distanceBR)
    # distanceBR= normalize(distanceBR)
    # print(distanceTL, distanceTR, distanceBL, distanceBR)

    # print(cornerVectorTL, cornerVectorTR, cornerVectorBL, cornerVectorBR)
    #calculate dot product of gradient vector at each of four corners
    #and distance vector (distance from corner point to target point)
    vecTL = calcDotProduct(cornerVectorTL, distanceTL)
    vecTR = calcDotProduct(cornerVectorTR, distanceTR)
    vecBL = calcDotProduct(cornerVectorBL, distanceBL)
    vecBR = calcDotProduct(cornerVectorBR, distanceBR)
    # print(vecTL, vecTR, vecBL, vecBR)

    #average TL and TR
    x1 = col
    # print(x - x1)
    Sx = 3 * (x - x1)**2 -  2 * (x - x1)**3
    a = interpolate(vecTL, vecTR, Sx)
    b = interpolate(vecBL, vecBR, Sx)
    # print(a, b)
    y1 = (row + 1)
    Sy = 3*(y - y1)**2 - 2*(y - y1)**3
    
    final = interpolate(a, b, Sy)
    #code to keep final result between (0 ,1) from:
    #http://adrianb.io/2014/08/09/perlinnoise.html
    return (final + 0.5)/1.5


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

def fillPerlinBoard(app):
    for pX in range(0, app.perlinBoardLength):
        for pY in range(0, app.perlinBoardLength):
            val = perlin(app, pX, pY)
            app.perlinBoard[pX][pY] = val

def perlinOctave2(app):
    #"Scale" it to half the size?
    #uhh so I should create another perlin board but half the size
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = perlin(app, pX, pY)
            app.newPerlinBoard[pX][pY] = val

def perlinOctave3(app):
    for pX in range(0, app.oct3PerlinLength):
        for pY in range(0, app.oct3PerlinLength):
            val = perlin(app, pX, pY)
            app.oct3PerlinBoard[pX][pY] = val

def perlinOctave4(app):
    for pX in range(0, app.oct4PerlinLength):
        for pY in range(0, app.oct4PerlinLength):
            val = perlin(app, pX, pY)
            app.oct4PerlinBoard[pX][pY] = val


def rgb_color(rgb):
    return '#%02x%02x%02x' % rgb

def drawPerlin(app, canvas, x, y):
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill = "black")

def movePerlin(app):
    tempBoard = copy.deepcopy(app.perlinBoard)
    for pX in range(0, 49):
        for pY in range(0, 49):
            newX, newY = 0, 0
            if (pX == 0):
                newX = 49
            elif (pY == 0):
                newY = 49
            else: 
                newY = pY - 1
            tempBoard[pX][pY] = app.perlinBoard[newX][newY]
    app.perlinBoard = tempBoard

print(rgb_color((200, 100, 25)))
def redrawAll(app, canvas):
    #Create another Perlin curve (or reuse the same one), but double the resolution
    #Then halve the output value, and add it on top of the first curve
    # for pX in range(0, app.perlinBoardLength):
    #     for pY in range(0, app.perlinBoardLength):
    #         val = app.perlinBoard[pX][pY]
    #         # print(val)
    #         val = int(abs(val) * 255) % 255
    #         #do some multiply blending here or smthn?
    #         color = rgb_color((val, val, val))
    #         offset = app.width // app.perlinBoardLength
    #         canvas.create_rectangle(pX * offset - offset, pY * offset - offset, pX * offset + offset, pY * offset + offset, fill = color)
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = app.newPerlinBoard[pX][pY]
            val2 = app.perlinBoard[pX//2][pY//2]
            val3 = app.oct3PerlinBoard[pX//4][pY//4]
            val4 = app.oct4PerlinBoard[pX//10][pY//10]
            # val = val4 + (val * 0.1) + (val2 * 0.2) + (val3 * 0.4)
            # val = (val + 1)/2
            # val = val/1.7
            # print(val)
            val = int(abs(val) * 255) % 255
            val2 = int(abs(val2) * 255) % 255
            val3 = int(abs(val3) * 255) % 255
            val4 = int(abs(val4) * 255) % 255
            val = val4 + val * 0.1
            # print(val, val2, val3, val4)
            # if (val > 255):
            #     val = 255
            val = int(val)
            #do some multiply blending here or smthn?
            color = rgb_color((val, val, val))
            offset = app.width // app.newPerlinLength
            canvas.create_rectangle(pX * offset - offset, pY * offset - offset, pX * offset + offset, pY * offset + offset, fill = color, width = 0)


runApp(width = 500, height = 500)
