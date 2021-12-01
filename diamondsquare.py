import random

#-----------------------------------------------------------
# DIAMOND SQUARE FUNCTIONS
#-----------------------------------------------------------

#Recursively performs square step and diamond step until board is filled
def diamondSquare(app, step, board):
    if (step == 0):
        return board
    else:
        for i in range(0, len(app.squareList), 4):
            #get four points of square 
            topLeftRow, topLeftCol = app.squareList[i]
            bottomLeftRow, bottomLeftCol = app.squareList[i + 1]
            bottomRightRow, bottomRightCol = app.squareList[i + 2]
            topRightRow, topRightCol = app.squareList[i + 3]
            average = (board[topLeftRow][topLeftCol] +
             board[bottomLeftRow][bottomLeftCol] 
             + board[bottomRightRow][bottomRightCol] 
             + board[topRightRow][topRightCol])//4
            #find average of four corners, add a random value to it
            average += random.randint(0, 10) 
            centerRow = app.squareList[i][0] + step
            centerCol = app.squareList[i][1] + step
            board[centerRow][centerCol] = average
            #square step
            center = (centerRow, centerCol)
            calculateDiamondValues(app, i, center, step, board) 
            addSquaresToList(app, i, center, step, board) 
        sol = diamondSquare(app, step//2, board)
        return sol

#fill "diamond" extending out from center with average of values near it
def calculateDiamondValues(app, i, center, step, board):
    #first find four corners of square
    tLRow, tLCol = app.squareList[i]
    bLRow, bLCol = app.squareList[i + 1]
    bRRow, bRCol = app.squareList[i + 2]
    tRRow, tRCol = app.squareList[i + 3]


    cRow, cCol = center
    dlRow, dlCol = cRow, cCol - step
    board[dlRow][dlCol]=(board[tLRow][tLCol] 
                                    + board[bLRow][bLCol] +
                                      board[cRow][cCol])//3
    #diamondBottom
    board[cRow + step][cCol]= (board[bRRow][bRCol] 
                                    + board[bLRow][bLCol] + 
                                    board[cRow][cCol])//3
    #diamondRight
    board[cRow][cCol + step] = (board[tRRow][tRCol] + 
                                    board[bLRow][bLCol] + 
                                    board[cRow][cCol])//3
    #diamondTop
    board[cRow - step][cCol] = (board[tLRow][tLCol] + 
                                    board[tRRow][tRCol] + 
                                    board[cRow][cCol])//3


#add squares to center list
def addSquaresToList(app, i, center, step, board):
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
                        
def createNewDiamondSquare(app):
    chunkSize = 33
    newBoard = [[0] * chunkSize for row in range(chunkSize)] 
    newBoard[0][0] = 15
    newBoard[chunkSize - 1][0] = 5
    newBoard[chunkSize - 1][chunkSize - 1] = 9
    newBoard[0][chunkSize - 1] = 7
    #change squarelist so it works
    app.squareList = [(0, 0), (chunkSize - 1, 0), 
                        (chunkSize - 1, chunkSize - 1), (0, chunkSize - 1)]
    return newBoard
