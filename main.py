from cmu_112_graphics import *
import random
import pygame


#for tp0: get infinite generation, player movement, isometric in
#for tp1: cloud generation, grass generation
#for tp2: dialogue w player, bird algortihm
#for tp3: yeah idk

#Credits: a bunch of code from my hack112 project
#Isometric code from: https://gamedevelopment.tutsplus.com/tutorials/creating-ismj
# ometric-worlds-a-primer-for-game-developers--gamedev-6511
#Diamond square algorithm: https://web.archive.org/web/20060420054134/http://www
# .gameprogrammer.com/fractal.html#diamond
#Perlin noise
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
    #CHANGE THIS TO ANY NUM X WHERE X = 2^n + 1 TO CHANGE ALL OTHER VARS
    app.rows = 33
    app.cols = app.rows
    app.board = [[0] * app.rows for row in range(app.rows)] #rows, cols have to be size 2^n + 1
    #colorboard stores colors, app.board stores height
    app.colorboard = [[0] * app.rows for row in range(app.rows)]


    app.cellSize = 100
    app.margin = 10
    #initialize corner values
    app.board[0][0] = 15
    app.board[app.rows - 1][0] = 5
    app.board[app.rows - 1][app.rows - 1] = 9
    app.board[0][app.rows - 1] = 7
    app.prevX = 200
    app.prevY = 100
    app.heightFac = 5
    #now you have 32 squares, perform diamond step again (find midpoint of all 32 squares)
    app.squareList = [(0, 0), (app.rows - 1, 0), (app.rows - 1, app.rows - 1), (0, app.rows - 1)]
    diamondSquare(app, app.rows//2)

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
    app.text = ""
    app.displayJournal = False
    app.journal = dict()
    app.goHome = False
    app.month = 6
    app.day = 1
    gameMode_fillBoard(app)


def restartApp(app):
    appStarted(app)
    
def diamondSquare(app, step):
    if (step == 0):
        return
    else:
        rows, cols = len(app.board), len(app.board[0])
        #go through each "square" and calculate center points, then find diamond, then add new squares into list
        for i in range(0, len(app.squareList), 4):
            #get four points of square - squarelist stores them (very badly)
            #in four tuples
            topLeftRow, topLeftCol = app.squareList[i]
            bottomLeftRow, bottomLeftCol = app.squareList[i + 1]
            bottomRightRow, bottomRightCol = app.squareList[i + 2]
            topRightRow, topRightCol = app.squareList[i + 3]
            average = (app.board[topLeftRow][topLeftCol] + app.board[bottomLeftRow][bottomLeftCol] + app.board[bottomRightRow][bottomRightCol] + app.board[topRightRow][topRightCol])//4
            #find average of four corners, add a random value to it
            average += random.randint(0, 10) 
            centerRow, centerCol = app.squareList[i][0] + step, app.squareList[i][1] + step
            app.board[centerRow][centerCol] = average
            #NOW do square step
            #center is step distance away from upper left square
            center = (centerRow, centerCol)
            calculateDiamondValues(app, i, center, step) #fill "diamond" extending out from center with average of values near it
            addSquaresToList(app, i, center, step) #add squares to center list
        diamondSquare(app, step//2)


def calculateDiamondValues(app, i, center, step):
    #first find four corners of square
    topLeftRow, topLeftCol = app.squareList[i]
    bottomLeftRow, bottomLeftCol = app.squareList[i + 1]
    bottomRightRow, bottomRightCol = app.squareList[i + 2]
    topRightRow, topRightCol = app.squareList[i + 3]


    centerRow, centerCol = center
    diamondLeftRow, diamondLeftCol = centerRow, centerCol - step
    app.board[diamondLeftRow][diamondLeftCol] = (app.board[topLeftRow][topLeftCol] + app.board[bottomLeftRow][bottomLeftCol] + app.board[centerRow][centerCol])//3
    #diamondBottom
    app.board[centerRow + step][centerCol] = (app.board[bottomRightRow][bottomRightCol] + app.board[bottomLeftRow][bottomLeftCol] + app.board[centerRow][centerCol])//3
    #diamondRight
    app.board[centerRow][centerCol + step] = (app.board[topRightRow][topRightCol] + app.board[bottomLeftRow][bottomLeftCol] + app.board[centerRow][centerCol])//3
    #diamondTop
    app.board[centerRow - step][centerCol] = (app.board[topLeftRow][topLeftCol] + app.board[topRightRow][topRightCol] + app.board[centerRow][centerCol])//3



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
    app.squareList += [(topLeftRow, topLeftCol), (diamondLeftRow, diamondLeftCol), (centerRow, centerCol), (diamondRightRow, diamondRightCol)]
    app.squareList += [(diamondLeftRow, diamondLeftCol), (bottomLeftRow, bottomLeftCol), (diamondBotRow, diamondBotCol), (centerRow, centerCol)]
    app.squareList += [(diamondTopRow, diamondTopCol), (centerRow, centerCol), (diamondRightRow, diamondRightCol), (topRightRow, topRightCol)]
    app.squareList += [(centerRow, centerCol), (diamondBotRow, diamondBotCol), (bottomRightRow, bottomRightCol), (diamondLeftRow, diamondLeftCol)]



def gameMode_2DToIso(app, x, y):
    newX = (x - y)/2 + app.prevX
    newY = (x + y)/4 + app.prevY
    return newX, newY


def interpolate(app, x, y):
    #i kind of want it to interpolate between diff colors/ emotions
    pass

def gameMode_constraintsMet(app, row, col):
    return (row >= 0 and row < len(app.board) and col >= 0 and col < len(app.board[0]))

def gameMode_expandBoard(app, dir):
    row, col = app.playerPos
    # if (dir == "left"):
    #     app.board.append([0] * app.cols)
    #     gameMode_fillBoard(app)


def gameMode_keyPressed(app, event):
    cx, cy = app.playerPos
    if (app.goHome):
        if (event.key == "Y"):
            app.goHome = False
            restartApp(app)
    if (len(event.key) == 1):
        app.text += event.key
        app.displayText = False #this is kinda bad but whatever
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
        app.journal[date] = app.journal.get(date, "") + app.text #not sure how to do this for several "days"
        app.text = ""
        app.displayJournal = not app.displayJournal #False -> True, True -> False
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

def getCellBoundsinCartesianCoords(app, canvas, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    return x0, y0, x1, y1
    
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

    # canvas.create_polygon(topX, topY, rightX, rightY, 
    #                         botX, botY, leftX, leftY, fill = color )
    # canvas.create_line(topX, topY, rightX, rightY, width = 2)
    # canvas.create_line(rightX, rightY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, topX, topY, width = 2)

    #each corner's y is different


    #get center of square in cartesian coordinates
    # x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, canvas, row, col)
    # cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    # cx, cy = gameMode_2DToIso(app, cx, cy)
    # cy -= app.board[row][col] #move cy up by height
    # canvas.create_oval(cx - 1, cy - 1, cx + 1, cy + 1, fill = "black")

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

    canvas.create_polygon(leftX, leftY, leftX, leftY - yOffsetTopL, 
                        botX, botY - yOffsetTopR, botX, botY, fill = color )
    canvas.create_polygon(botX, botY, botX, botY - yOffsetTopR, 
                            rightX, rightY - yOffsetTopL, rightX, rightY, fill = color )
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
    # leftY -= yOffsetTopL
    # topY -= yOffsetTopL
    # botY -= yOffsetTopL
    # rightY -= yOffsetTopL
    #this did noooot work
    leftY -= yOffsetTopL
    topY -= yOffsetBotL
    botY -= yOffsetTopR
    rightY -= yOffsetBotR
    #draw "box" ????? 
    # print(row, col, "TopL", leftX, leftY, "\n", "TopR",  topX, topY, "\n", "botL", botX, botY, "\n", "botR",  rightY)

    #draw "height" (top plane of box)
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = color )

    canvas.create_line(topX, topY, rightX, rightY, width = 2)
    canvas.create_line(rightX, rightY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, topX, topY, width = 2)
    cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    cx, cy = gameMode_2DToIso(app, cx, cy)
    # canvas.create_text(cx, cy, text = f"{row}{col}")
    # canvas.create_text(topX, topY, text = f"{topY}")
    # canvas.create_text(leftX, leftY, text = f"{leftY}", fill = "white")
    # canvas.create_text(rightX, rightY, text = f"{rightY}")
    # canvas.create_text(botX, botY, text = f"{botY}")



def gameMode_drawPlayer(app, canvas):
    row, col = app.playerPos
    x = col * app.cellSize
    y = row * app.cellSize
    yOffset = app.board[row][col] * app.heightFac
    x, y = gameMode_2DToIso(app, x, y)
    y += app.cellSize//2
    # y -= yOffset//2
    canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill = "white")
    #gameMode_drawCell(app, canvas, row, col, "white")

def gameMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    canvas.create_text(app.width/2, app.height/2, text = "you went home for the day and rested")
    canvas.create_text(app.width/2, app.height/2 + 20, text = "go out again the next morning? (y/n)")

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

def gameMode_drawJournal(app, canvas):
    canvas.create_rectangle(200, 200, 600, 600, fill = "#f5eace")
    canvas.create_text(220, 400, text = "daily journal", font = "Courier 24 bold")
    i = 0
    for key in app.journal:
        tex = app.journal[key]
        canvas.create_text(200 + i * 20, 400, text = tex)
        i += 1

def gameMode_drawTextBubble(app, canvas):
    canvas.create_text(app.width//2, 700, text = f"{app.text}", fill = "white",
                        font = "Courier 24 bold")

def gameMode_drawHills(app, canvas):
    #diamond square algorithm
    pass

def gameMode_drawGrass(app, canvas, row, col):
    #draw 5 grass things
    x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, canvas, row, col)
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

    

def gameMode_drawTrees(app, canvas):
    pass

def gameMode_drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#94c4f7")
    increment = app.height/4
    for i in range(4):
        y = i * increment
        canvas.create_rectangle(0, y - increment, 0, y, fill = app.skyColor[i] )



def gameMode_redrawAll(app, canvas):
    if (app.displayJournal):
        gameMode_drawJournal(app, canvas)
    else:
        gameMode_drawBackground(app, canvas)
        gameMode_drawBoard(app, canvas) 
        gameMode_drawPlayer(app, canvas)
        gameMode_drawTextBubble(app, canvas)
    # gameMode_drawObstacles(app, canvas)

runApp(width = 800, height = 800)