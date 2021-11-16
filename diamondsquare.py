from cmu_112_graphics import *
import random

#credits: me, hopefully
def appStarted(app):
    app.board = [[0] * 5 for row in range(5)] #rows, cols have to be size 2^n + 1
    app.rows = 5
    app.cols = 5
    app.cellSize = 40
    app.margin = 10
    #initialize corner values
    app.board[0][0] = 4
    app.board[4][0] = 5
    app.board[4][4] = 6
    app.board[0][4] = 7
    app.prevX = 200
    app.prevY = 100
    #now you have 4 squares, perform diamond step again (find midpoint of all 4 squares)
    app.squareList = [(0, 0), (4, 0), (4, 4), (0, 4)]
    diamondSquare(app, 2)

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

def diamondSquare(app, step, depth = 0):
    if (step == 0):
        print(print2dList(app.board))
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
            # average += random.randint(0, 10) 
            centerRow, centerCol = app.squareList[i][0] + step, app.squareList[i][1] + step
            app.board[centerRow][centerCol] = average
            #NOW do square step
            #center is step distance away from upper left square
            center = (centerRow, centerCol)
            calculateDiamondValues(app, i, center, step) #fill "diamond" extending out from center with average of values near it
            addSquaresToList(app, i, center, step) #add squares to center list
            print("  " * depth, print2dList(app.board))
        diamondSquare(app, step//2, depth + 1)


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


def drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def TwoDToIso(app, x, y):
    newX = (x - y)/2 + app.prevX
    newY = (x + y)/4 + app.prevY
    return newX, newY


def getCellBoundsinCartesianCoords(app, canvas, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    return x0, y0, x1, y1
    
def drawCell(app, canvas, row, col, color):
    x0 = col * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    #convert to isometric coords
    leftX, leftY = TwoDToIso(app, x0, y0)
    topX, topY = TwoDToIso(app, x0, y1)
    botX, botY = TwoDToIso(app, x1, y0)  
    rightX,rightY = TwoDToIso(app, x1, y1)
    yOffset = app.board[row][col] 
    #i can change "height" of hills by changing offset :thinking: 

    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = "blue" )
    # canvas.create_line(topX, topY, rightX, rightY, width = 2)
    # canvas.create_line(rightX, rightY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, botX, botY, width = 2)
    # canvas.create_line(leftX, leftY, topX, topY, width = 2)


    #create a "box" lol... this might be too much computations going on
    canvas.create_polygon(leftX, leftY, leftX, leftY - yOffset, 
                        botX, botY - yOffset, botX, botY, fill = "blue" )
    canvas.create_polygon(botX, botY, botX, botY - yOffset, 
                            rightX, rightY - yOffset, rightX, rightY, fill = "blue" )
    canvas.create_polygon(botX, botY, botX, botY - yOffset, 
                            topX, topY - yOffset, topX, topY, fill = "blue" )
    canvas.create_line(topX, topY, topX, topY - yOffset, width = 2)
    canvas.create_line(rightX, rightY, rightX, rightY - yOffset, width = 2)
    canvas.create_line(leftX, leftY, leftX, leftY - yOffset, width = 2)
    canvas.create_line(botX, botY, botX, botY - yOffset, width = 2)

    # canvas.create_polygon(topX, topY, rightX, rightY, 
    #                         botX, botY, leftX, leftY, fill = "blue" )
    # canvas.create_polygon(topX, topY, rightX, rightY, 
    #                         botX, botY, leftX, leftY, fill = "blue" )

    #get center of square in cartesian coordinates
    # x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, canvas, row, col)
    # cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    # cx, cy = TwoDToIso(app, cx, cy)
    # cy -= app.board[row][col] #move cy up by height
    # canvas.create_oval(cx - 1, cy - 1, cx + 1, cy + 1, fill = "black")
    leftX, leftY = TwoDToIso(app, x0, y0)
    topX, topY = TwoDToIso(app, x0, y1)
    botX, botY = TwoDToIso(app, x1, y0)  
    rightX, rightY = TwoDToIso(app, x1, y1)
    leftY -= yOffset
    topY -= yOffset
    botY -= yOffset
    rightY -= yOffset

    #draw "height"
    canvas.create_polygon(topX, topY, rightX, rightY, 
                            botX, botY, leftX, leftY, fill = "blue" )
    canvas.create_line(topX, topY, rightX, rightY, width = 2)
    canvas.create_line(rightX, rightY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, botX, botY, width = 2)
    canvas.create_line(leftX, leftY, topX, topY, width = 2)


def drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def redrawAll(app, canvas):
    drawBoard(app, canvas)

runApp(width = 400, height = 400)