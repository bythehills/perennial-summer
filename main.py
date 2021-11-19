from cmu_112_graphics import *
import random


#Credits: Code for drawBoard, fillBoard, drawPlayer, keyPressed, drawCell
# taken from code I wrote for hack112 
#2dToIso (175) from: https://gamedevelopment.tutsplus.com/tutorials/creating-ism
# jometric-worlds-a-primer-for-game-developers--gamedev-6511
#Diamond square algorithm: https://web.archive.org/web/20060420054134/http://www
# .gameprogrammer.com/fractal.html#diamond
#Perlin noise from https://web.archive.org/web/20170201233641/https://mzucker.gi
# thub.io/html/perlin-noise-math-faq.html
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

#Initialize vars
def appStarted(app):
    app.text = ""
    app.displayJournal = False
    app.goHome = False
    restartApp(app)



#"Restarts" app, including player pos, but keeps journal
def restartApp(app):
    app.mode = "gameMode"
    #change this to any num x where x = 2^n + 1
    app.rows = 33
    app.cols = app.rows
    app.board = [[0] * app.rows for row in range(app.rows)] 
    #colorboard stores colors, app.board stores height
    app.colorboard = [[0] * app.rows for row in range(app.rows)]
    app.cellSize = 100
    app.margin = 0

    #Diamond square algorithm 
    #initialize corner values
    app.board[0][0] = 15
    app.board[app.rows - 1][0] = 5
    app.board[app.rows - 1][app.rows - 1] = 9
    app.board[0][app.rows - 1] = 7
    app.prevX = 200
    app.prevY = 100
    app.heightFac = 5
    app.squareList = [(0, 0), (app.rows - 1, 0), 
                        (app.rows - 1, app.rows - 1), (0, app.rows - 1)]
    diamondSquare(app, app.rows//2)

    #Color, position
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

    #Vars related to journal
    #BRUH HOW TF DOES RESTARTAPP WORK
    app.journal = dict()
    app.month = 6
    app.day = 1

    #vars related to perlin noise
    app.perlinRows = 50
    app.perlinCols = app.perlinRows
    app.gradBoard = [[(0, 0)] * app.perlinRows for row in range(app.perlinRows)]
    app.perlinCellSize = 5 #idk why this can never be less than 5..
    app.perlinBoardLength = 50
    app.perlinBoard = [[0] * app.perlinBoardLength 
                        for row in range(app.perlinBoardLength)]
    app.newPerlinBoard = [[0] * (app.perlinBoardLength* 2) 
                            for row in range(app.perlinBoardLength * 2)]
    app.newPerlinLength = app.perlinBoardLength * 2
    app.oct3PerlinBoard = [[0] * (app.perlinBoardLength//2) 
                            for row in range(app.perlinBoardLength//2)]
    app.oct3PerlinLength = app.perlinBoardLength//2

    calcGradVec(app, app.perlinBoard)

    fillPerlinBoard(app)
    perlinOctave2(app)
    perlinOctave3(app)

    gameMode_fillBoard(app)

#-----------------------------------------------------------
# PERLIN FUNCTIONS
#-----------------------------------------------------------

def calcGradVec(app, board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            dx = random.randrange(0, 100)
            dx = float(dx/100)
            a2 = dx**2
            b2 = (1 - a2) ** 0.5
            dy = b2
            chance = random.randint(0, 3)
            if (chance == 1):
                board[row][col] = (dx, dy)
            elif (chance == 2):
                board[row][col] = (-dx, dy)
            elif (chance == 3):
                board[row][col] = (-dx, -dy)
            else:
                board[row][col] = (dx, -dy )

def calcDotProduct(corner, cur):
    a, b = corner
    c, d, = cur
    return (a * c + b * d)

def interpolate(a, b, t):
    return a + t *(b  - a)

def perlin(app, x, y):
    #for every pixel, calculate distance from four points
    #REMINDER: COL IS X, ROW IS Y
    col = int((x - app.margin)//app.perlinCellSize) 
    row = int((y - app.margin)//app.perlinCellSize) 
    cornerVectorTL = app.gradBoard[row][col]
    #Turn (x, y) into decimal points
    x = float(x/app.perlinCellSize)
    y = float(y/app.perlinCellSize)
    distanceTL = (x - col, y - row)
    #Calculate corner gradient vectors and distance from (x, y)
    if (col + 1 < app.perlinCols):
        cornerVectorTR = app.gradBoard[row][col + 1]
        distanceTR = (x - col - 1, y - row)
    else:
        cornerVectorTR = cornerVectorTL
        distanceTR = distanceTL
    
    if (row + 1 < app.perlinRows):
        cornerVectorBL = app.gradBoard[row + 1][col]
        distanceBL = (x - col, y - row - 1)

    else:
        cornerVectorBL = cornerVectorTL
        distanceBL = distanceTL

    
    if (row + 1 < app.perlinRows and col + 1 < app.perlinCols):
        cornerVectorBR = app.gradBoard[row + 1][col + 1]
        distanceBR = (x - col - 1, y - row - 1)

    else:
        cornerVectorBR = cornerVectorTL
        distanceBR = distanceTL

    #calculate dot product of gradient vector at each of four corners
    #and distance vector (distance from corner point to target point)
    vecTL = calcDotProduct(cornerVectorTL, distanceTL)
    vecTR = calcDotProduct(cornerVectorTR, distanceTR)
    vecBL = calcDotProduct(cornerVectorBL, distanceBL)
    vecBR = calcDotProduct(cornerVectorBR, distanceBR)

    #average TL and TR
    x1 = col
    Sx = 3 * (x - x1)**2 -  2 * (x - x1)**3
    a = interpolate(vecTL, vecTR, Sx)
    b = interpolate(vecBL, vecBR, Sx)
    y1 = row
    Sy = 3*(y - y1)**2 - 2*(y - y1)**3
    
    final = interpolate(a, b, Sy)

    #code to keep final result between (0 ,1) from:
    #http://adrianb.io/2014/08/09/perlinnoise.html
    return (final + 0.3)

def fillPerlinBoard(app):
    for pX in range(0, app.perlinBoardLength):
        for pY in range(0, app.perlinBoardLength):
            val = perlin(app, pX, pY)
            app.perlinBoard[pX][pY] = val

def perlinOctave2(app):
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = perlin(app, pX, pY)
            app.newPerlinBoard[pX][pY] = val

def perlinOctave3(app):
    for pX in range(0, app.oct3PerlinLength):
        for pY in range(0, app.oct3PerlinLength):
            val = perlin(app, pX, pY)
            app.oct3PerlinBoard[pX][pY] = val

#-----------------------------------------------------------
# DIAMOND SQUARE FUNCTIONS
#-----------------------------------------------------------

#Recursively performs square step and diamond step until board is filled
def diamondSquare(app, step):
    if (step == 0):
        return 
    else:
        rows, cols = len(app.board), len(app.board[0])
        for i in range(0, len(app.squareList), 4):
            #get four points of square 
            topLeftRow, topLeftCol = app.squareList[i]
            bottomLeftRow, bottomLeftCol = app.squareList[i + 1]
            bottomRightRow, bottomRightCol = app.squareList[i + 2]
            topRightRow, topRightCol = app.squareList[i + 3]
            average = (app.board[topLeftRow][topLeftCol] +
             app.board[bottomLeftRow][bottomLeftCol] 
             + app.board[bottomRightRow][bottomRightCol] 
             + app.board[topRightRow][topRightCol])//4
            #find average of four corners, add a random value to it
            average += random.randint(0, 10) 
            centerRow = app.squareList[i][0] + step
            centerCol = app.squareList[i][1] + step
            app.board[centerRow][centerCol] = average

            #square step
            center = (centerRow, centerCol)
            calculateDiamondValues(app, i, center, step) 
            addSquaresToList(app, i, center, step) 
        diamondSquare(app, step//2)

#fill "diamond" extending out from center with average of values near it
def calculateDiamondValues(app, i, center, step):
    #first find four corners of square
    tLRow, tLCol = app.squareList[i]
    bLRow, bLCol = app.squareList[i + 1]
    bRRow, bRCol = app.squareList[i + 2]
    tRRow, tRCol = app.squareList[i + 3]


    cRow, cCol = center
    dlRow, dlCol = cRow, cCol - step
    app.board[dlRow][dlCol]=(app.board[tLRow][tLCol] 
                                    + app.board[bLRow][bLCol] +
                                      app.board[cRow][cCol])//3
    #diamondBottom
    app.board[cRow + step][cCol]= (app.board[bRRow][bRCol] 
                                    + app.board[bLRow][bLCol] + 
                                    app.board[cRow][cCol])//3
    #diamondRight
    app.board[cRow][cCol + step] = (app.board[tRRow][tRCol] + 
                                    app.board[bLRow][bLCol] + 
                                    app.board[cRow][cCol])//3
    #diamondTop
    app.board[cRow - step][cCol] = (app.board[tLRow][tLCol] + 
                                    app.board[tRRow][tRCol] + 
                                    app.board[cRow][cCol])//3


#add squares to center list
def addSquaresToList(app, i, center, step):
    topLeftRow, topLeftCol = app.squareList[i]
    bottomLeftRow, bottomLeftCol = app.squareList[i + 1]
    bottomRightRow, bottomRightCol = app.squareList[i + 2]
    topRightRow, topRightCol = app.squareList[i + 3]

    centerRow, centerCol = center
    diamondLeftRow, diamondLeftCol = centerRow, centerCol - step
    diamondRightRow, diamondRightCol = centerRow, centerCol + step
    diamondBotRow, diamondBotCol = centerRow + step, centerCol
    diamondTopRow, diamondTopCol = centerRow - step, centerCol

    #add four squares for each "center" given
    app.squareList += [(topLeftRow, topLeftCol), 
                        (diamondLeftRow, diamondLeftCol), 
                        (centerRow, centerCol),
                        (diamondRightRow, diamondRightCol)]

    app.squareList += [(diamondLeftRow, diamondLeftCol), 
                        (bottomLeftRow, bottomLeftCol), 
                        (diamondBotRow, diamondBotCol), 
                        (centerRow, centerCol)]
    app.squareList += [(diamondTopRow, diamondTopCol), 
                        (centerRow, centerCol), 
                        (diamondRightRow, diamondRightCol), 
                        (topRightRow, topRightCol)]
    app.squareList += [(centerRow, centerCol), 
                        (diamondBotRow, diamondBotCol), 
                        (bottomRightRow, bottomRightCol), 
                        (diamondLeftRow, diamondLeftCol)]

#Credits see top
def gameMode_2DToIso(app, x, y):
    newX = (x - y)/2 + app.prevX
    newY = (x + y)/4 + app.prevY
    return newX, newY

#Interpolate between colors (to be implemented)
def interpolate(app, x, y):
    pass

#Checks for player movement
def gameMode_constraintsMet(app, r, c):
    return (r >= 0 and r < len(app.board) and c >= 0 and c < len(app.board[0]))

#To be implemented
def gameMode_expandBoard(app, dir):
    row, col = app.playerPos


def gameMode_keyPressed(app, event):
    cx, cy = app.playerPos
    #Journal input
    if (app.goHome):
        if (event.key == "y"):
            app.goHome = False
            appStarted(app)
    if (len(event.key) == 1):
        app.text += event.key
        app.displayJournal = False 
    if (event.key == "Space"):
        app.text += " "
    if (app.text.lower() == "go home"):
        app.goHome = True
        app.text = ""
        app.day += 1
        if (app.day >= 30):
            app.month += 1
            app.day = 1
    if (event.key == 'Enter'):
        date = f"{app.month}/{app.day}"
        app.journal[date] = app.journal.get(date, "") + "\n" + app.text 
        app.text = ""
        app.displayJournal = not app.displayJournal 

    #Player movement
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

def getCellBoundsinCartesianCoords(app, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    return x0, y0, x1, y1

#Draws terrain according to height
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

    #This draws "base", kept for testing purpsoes
    # canvas.create_polygon(topX, topY, rightX, rightY, 
    #                         botX, botY, leftX, leftY, fill = color )
    # canvas.create_line(topX, topY, rightX, rightY, width = 2)
    # canvas.create_line(rightX, rightY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, topX, topY, width = 2)

    #Draw height
    leftX, leftY = gameMode_2DToIso(app, x0, y0)
    topX, topY = gameMode_2DToIso(app, x0, y1)
    botX, botY = gameMode_2DToIso(app, x1, y0)  
    rightX, rightY = gameMode_2DToIso(app, x1, y1)
    yOffsetTopL = app.board[row][col] * app.heightFac
    if (row + 1 < app.rows):
        yOffsetBotL = app.board[row + 1][col] * app.heightFac
    else:
        yOffsetBotL = yOffsetTopL
    
    if (col + 1 < app.cols):
        yOffsetTopR = app.board[row][col + 1] * app.heightFac
    else:
        yOffsetTopR = yOffsetTopL
    
    if (row + 1 < app.rows and col + 1 < app.cols):
        yOffsetBotR = app.board[row + 1][col + 1] * app.heightFac
    else:
        yOffsetBotR = yOffsetTopL

    #Draws sides
    canvas.create_polygon(leftX, leftY, leftX, leftY - yOffsetTopL, 
                        botX, botY - yOffsetTopR, botX, botY, fill = color )
    canvas.create_polygon(botX, botY, botX, botY - yOffsetTopR, 
                            rightX, rightY - yOffsetTopL, rightX, rightY, 
                            fill = color )
    canvas.create_polygon(botX, botY, botX, botY - yOffsetTopR, 
                            topX, topY - yOffsetBotL, topX, topY, fill = color )
    canvas.create_line(topX, topY, topX, topY - yOffsetBotL, width = 2)
    canvas.create_line(rightX, rightY, rightX, rightY - yOffsetBotR, width = 2)
    canvas.create_line(leftX, leftY, leftX, leftY - yOffsetTopL, width = 2)
    canvas.create_line(botX, botY, botX, botY - yOffsetTopR, width = 2)
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = color )
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = color )
    leftY -= yOffsetTopL
    topY -= yOffsetBotL
    botY -= yOffsetTopR
    rightY -= yOffsetBotR

    #Draws "height" (top plane of box)
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = color )

    canvas.create_line(topX, topY, rightX, rightY, width = 2)
    canvas.create_line(rightX, rightY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, topX, topY, width = 2)
    cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    cx, cy = gameMode_2DToIso(app, cx, cy)


def gameMode_drawPerlin(app, canvas):
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = app.newPerlinBoard[pX][pY]
            val2 = app.perlinBoard[pX//2][pY//2]
            val3 = app.oct3PerlinBoard[pX//4][pY//4]
            val4 = app.oct4PerlinBoard[pX//10][pY//10]
            val = (val * 0.5) + (val2 * 0.5) + val3
            val = int((val) * 255)

            #Clamp it between black and white
            if (val >= 255):
                val = 255
            elif (val <= 0):
                val = 0
            
            color = 0
            if (val >= 200):
                color = "#ffffff"
            elif (val >= 180):
                color = "#e8f1fc"
            elif (val >= 150):
                color = "#deecfc"
            elif (val >= 120):
                color = "#dae8f0"
            elif (val >= 80):
                color = "#7ab7f0"
            else:
                color = "#7ab7f0"
            # color = rgb_color((val, val, val))
            offset = app.width // app.newPerlinLength
            canvas.create_rectangle(pX * offset - offset, pY * offset - offset, 
                                    pX * offset + offset, pY * offset + offset, 
                                    fill = color, width = 0)


def gameMode_drawPlayer(app, canvas):
    row, col = app.playerPos
    x = col * app.cellSize
    y = row * app.cellSize
    yOffset = app.board[row][col] * app.heightFac
    x, y = gameMode_2DToIso(app, x, y)
    y += app.cellSize//2
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill = "white")

def gameMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    canvas.create_text(app.width/2, app.height/2, 
                        text = "you went home for the day and rested", 
                        fill = "white")
    canvas.create_text(app.width/2, app.height/2 + 20, 
                        text = "go out again the next morning? (y/n)",
                        fill = "white")

#Fills board at beginning with colors, also called whenever new rows are added
def gameMode_fillBoard(app):
    rows, cols = len(app.colorboard), len(app.colorboard[0])
    for row in range(rows):
        for col in range(cols):
            if app.colorboard[row][col] == 0:
                index = random.randint(0, len(app.color) - 1)
                app.colorboard[row][col] = app.color[index]
            

def gameMode_drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            gameMode_drawCell(app, canvas, row, col, app.colorboard[row][col])
            # if (row == 3):
            #     gameMode_drawGrass(app, canvas, row, col)

#From hack112 
# def gameMode_drawObstacles(app, canvas):
#     for obs in app.obsList:
#         row, col = obs.row, obs.col
#         #get x, y of row, col
#         x = col * app.cellSize
#         y = row * app.cellSize
#         x, y = gameMode_2DToIso(x, y)
#         counter = obs.spriteCounter

def gameMode_drawJournal(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#94c4f7")
    canvas.create_rectangle(100, 200, 700, 600, fill = "#f5eace")
    canvas.create_text(400, 220, text = "journal", 
                        font = "Courier 24 bold", anchor = "s")
    i = 0
    for key in app.journal:
        canvas.create_text (200, 250 + i * 20, text = key)
        tex = app.journal[key]
        for entry in tex.splitlines():
            canvas.create_text(200, 250 + i * 20, text = entry)
            i += 1

def gameMode_drawTextBubble(app, canvas):
    canvas.create_text(app.width//2, 700, text = f"{app.text}", fill = "white",
                        font = "Courier 24 bold", anchor = "s")


def gameMode_drawGrass(app, canvas, row, col):
    x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
    cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    cx, cy = gameMode_2DToIso(app, cx, cy)
    for _ in range(0, 3):
        cy -= app.board[row][col] * app.heightFac
        canvas.create_arc(cx - 20, cy - 20, cx, cy, style = CHORD, 
                            fill = "green", start = 110, width = 0)
        canvas.create_arc(cx , cy , cx + 20, cy + 20, style = CHORD, 
                        fill = "green", start = 120, width = 0)
        canvas.create_arc(cx - 10, cy - 10, cx + 10, cy + 10, style = CHORD, 
                            fill = "green", start = 150, width = 0)

    
#To be implemented w/ perlin
def gameMode_drawTrees(app, canvas):
    pass

def gameMode_drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#94c4f7")
    increment = app.height/4
    for i in range(4):
        y = i * increment
        canvas.create_rectangle(0, y - increment, 0, y, fill = app.skyColor[i])



def gameMode_redrawAll(app, canvas):
    if (app.displayJournal):
        gameMode_drawJournal(app, canvas)
    elif (app.goHome):
        gameMode_drawHome(app, canvas)
    else:
        gameMode_drawBackground(app, canvas)
        gameMode_drawBoard(app, canvas) 
        gameMode_drawPlayer(app, canvas)
        gameMode_drawTextBubble(app, canvas)
        gameMode_drawPerlin(app, canvas)
    # gameMode_drawObstacles(app, canvas)

runApp(width = 800, height = 800)