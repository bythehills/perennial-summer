from cmu_112_graphics import *
import random
import pygame


#for tp0: get infinite generation, player movement, isometric in
#for tp1: cloud generation, grass generation
#for tp2: dialogue w player, bird algortihm
#for tp3: yeah idk

#Credits: a bunch of code from my hack112 project
#Isometric code from: https://gamedevelopment.tutsplus.com/tutorials/creating-is
# ometric-worlds-a-primer-for-game-developers--gamedev-6511
#Diamond square algorithm: https://web.archive.org/web/20060420054134/http://www
# .gameprogrammer.com/fractal.html#diamond
#Perlin noise
#Voronoi / worley? for trees
#Cool clouds definitely not achievable though http://killzone.dl.playstation.net
# /killzone/horizonzerodawn/presentations/Siggraph15_Schneider_Real-Time_Volumet
# ric_Cloudscapes_of_Horizon_Zero_Dawn.pdf
#Repr2DList from : https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html

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

def appStarted(app):
    app.mode = "gameMode"
    app.cellSize = 100
    app.rows = 15    
    app.cols = 15
    app.margin = 0
    app.borderWidth = 10
    app.board = [[0] * app.cols for row in range(app.rows)]
    app.color = ["#649e44", "#2f5234", "#4d9129", "#1f6129", "#136b19"]
    app.timerCount = 0
    app.playerPos = (0, 0)
    app.obsList = [] #list of class obstalces
    app.lives = 3
    app.score = 0
    app.gameOver = False
    app.brdWidth = 0
    app.playerDir = ""
    app.prevX = 300
    app.prevY = 150
    app.skyColor = ["#6197ed", "#81a5de", "#aac0e3", "white" ]
    gameMode_fillBoard(app)



def gameMode_2DToIso(app, x, y):
    newX = (x - y)/2 + app.prevX
    newY = (x + y)/4 + app.prevY
    return newX, newY


def gameMode_IsoTo2D(x, y):
    newX = (x - y)/2 + 400
    newY = (x + y)/4 + 200
    return newX, newY

def gameMode_timerFired(app):
    row, col = app.playerPos
    pass

def gameMode_constraintsMet(app, row, col):
    return (row >= 0 and row < len(app.board) and col >= 0 and col < len(app.board[0]))

def gameMode_expandBoard(app, dir):
    row, col = app.playerPos
    if (dir == "left"):
        app.board.append([0] * app.cols)
        gameMode_fillBoard(app)


def gameMode_keyPressed(app, event):
    cx, cy = app.playerPos
    if (event.key == 'Up'):
        if (gameMode_constraintsMet(app, cx - 1, cy - 1)):
            app.prevY += 40
            app.playerPos = (cx - 1, cy - 1)
    elif (event.key == 'Down'):
        if (gameMode_constraintsMet(app, cx + 1, cy + 1)):
            app.prevY -= 40
            app.playerPos = (cx + 1, cy + 1)
    elif (event.key == 'Right'):
        if (gameMode_constraintsMet(app, cx - 1, cy)):
            app.playerPos = (cx - 1, cy)
            app.prevX -= 40
            app.playerDir = "right"
        gameMode_expandBoard(app, "right")
    elif (event.key == 'Left'):
        if (gameMode_constraintsMet(app, cx + 1, cy)):
            app.prevX += 40
            app.playerPos = (cx + 1, cy)
        gameMode_expandBoard(app, "left")

def gameMode_drawCell(app, canvas, row, col, color):
    x0 = col * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    #convert to isometric coords
    leftX, leftY = gameMode_2DToIso(app, x0, y0)
    topX, topY = gameMode_2DToIso(app, x0, y1)
    botX, botY = gameMode_2DToIso(app, x1, y0)  
    rightX,rightY = gameMode_2DToIso(app, x1, y1)
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = color )
    canvas.create_line(topX, topY, rightX, rightY, width = app.brdWidth)
    canvas.create_line(rightX, rightY, botX, botY, width = app.brdWidth)
    canvas.create_line(leftX, leftY, botX, botY, width = app.brdWidth)
    canvas.create_line(leftX, leftY, topX, topY, width = app.brdWidth)

def gameMode_drawPlayer(app, canvas):
    row, col = app.playerPos
    x = col * app.cellSize
    y = row * app.cellSize
    x, y = gameMode_2DToIso(app, x, y)
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill = "white")
    #gameMode_drawCell(app, canvas, row, col, "white")


#Fills board at beginning with colors, also called whenever new rows are added
def gameMode_fillBoard(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            if app.board[row][col] == 0:
                index = random.randint(0, len(app.color) - 1)
                app.board[row][col] = app.color[index]
            

def gameMode_drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            gameMode_drawCell(app, canvas, row, col, app.board[row][col])

# def gameMode_drawObstacles(app, canvas):
#     for obs in app.obsList:
#         row, col = obs.row, obs.col
#         #get x, y of row, col
#         x = col * app.cellSize
#         y = row * app.cellSize
#         x, y = gameMode_2DToIso(x, y)
#         counter = obs.spriteCounter

def gameMode_drawClouds(app, canvas):

    pass

def gameMode_drawHills(app, canvas):
    #diamond square algorithm
    pass

def gameMode_drawGrass(app, canvas):
    pass

def gameMode_drawTrees(app, canvas):
    pass

def gameMode_drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#94c4f7")
    increment = app.height/4
    for i in range(4):
        y = i * increment
        canvas.create_rectangle(0, y - increment, 0, y, fill = app.skyColor[i] )



def gameMode_redrawAll(app, canvas):
    gameMode_drawBackground(app, canvas)
    gameMode_drawBoard(app, canvas)
    gameMode_drawPlayer(app, canvas)
    # gameMode_drawObstacles(app, canvas)

runApp(width = 800, height = 800)