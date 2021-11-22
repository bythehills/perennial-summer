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
#Caching photoimages from : https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
#Code for opening / closing / writing / reading files adapted from : https://www.guru99.com/reading-and-writing-files-in-python.html
#AND https://stackoverflow.com/questions/28873349/python-readlines-not-returning-anything
#Getpixel and Putpixel from slfkjsldkjf
#Camera movement adapted from PIL/Pillow mini lecture


#Initialize vars
def appStarted(app):
    app.mode = "gameMode"
    #change this to any num x where x = 2^n + 1
    app.rows = 33
    app.cols = app.rows
    app.board = [[0] * app.rows for row in range(app.rows)] 
    #grassColorBoard stores colors, app.board stores height
    app.grassColorBoard = [[0] * app.rows for row in range(app.rows)]
    app.grassTreeBoard = copy.deepcopy(app.grassColorBoard)
    app.cellSize = 300
    app.margin = 0

    #Diamond square algorithm 
    #initialize corner values
    app.board[0][0] = 15
    app.board[app.rows - 1][0] = 5
    app.board[app.rows - 1][app.rows - 1] = 9
    app.board[0][app.rows - 1] = 7
    app.prevX = 200
    app.prevY = 100
    app.squareList = [(0, 0), (app.rows - 1, 0), 
                        (app.rows - 1, app.rows - 1), (0, app.rows - 1)]
    diamondSquare(app, app.rows//2)


    app.timerCount = 0
    app.playerPos = (700, 100)
    url = "playerSprite.png"
    app.playerSprite = app.loadImage(url)

    app.speed = 40
    app.obsList = [] #list of class obstalces
    app.lives = 3
    app.score = 0
    app.gameOver = False
    app.brdWidth = 0
    app.playerDir = ""
    app.prevX = 300
    app.prevY = 150
    app.skyColor = ["#6197ed"]
    app.timerDelay = 100
    app.timeSinceLastCloud = 0

    #JOURNAL VARS
    app.journal = open("journal.txt", "a+")
    app.date = open("date.txt", "r")
    app.feeling = open("feeling.txt", "r")
    #stores journal lines
    app.lines = []
    app.feelingsDict = dict() #stores counts of different "moods"
    app.text = ""
    app.textLenChecker = 0
    app.displayJournal = False
    app.goHome = False
    date = app.date.read()
    app.month, app.day = findDate(date)
    app.date.close()
    #when it starts u have to start w/ /6/1 on DATE.TXT, not JOURNAL.TXT
    #app.date updates with new day, write that day down
    app.journal.write(f"\n{app.month}/{app.day}\n") 
    url = "journalopen.png"
    app.journalOpenSprite = app.loadImage(url)
    url = "journalclose.png"
    app.journalCloseSprite = app.loadImage(url)
    app.vibe = app.feeling.read() #reads 'happy", "sad", "neutral", or "angry"

    #Vars related to tree or nature stuff
    url = "tree.png"
    app.treeSprite = app.loadImage(url)
    app.treeSprite = app.scaleImage(app.treeSprite, 0.5)
    url = "grass.png"
    app.grassSprite = app.loadImage(url)
    url = "neutralgrass.png"
    app.neutralGrassSprite = app.loadImage(url)
    url = "madgrass.png"
    app.madGrassSprite = app.loadImage(url)
    url = "sadgrass.png"
    app.sadGrassSprite = app.loadImage(url)

    url = "neutralFilter.png"
    app.neutralFilter = app.loadImage(url)
    app.neutralFilter = app.scaleImage(app.neutralFilter, 4)
    url = "sadFilter.png"
    app.sadFilter = app.loadImage(url)
    app.sadFilter = app.scaleImage(app.sadFilter, 4)
    url = "happyFilter.png"
    app.happyFilter = app.loadImage(url)
    app.happyFilter = app.scaleImage(app.happyFilter, 4)
    url = "madFilter.png"
    app.madFilter = app.loadImage(url)
    app.madFilter = app.scaleImage(app.madFilter, 4)



    #Color variations (for grass) to be implemented : color variations for
    #clouds, trees, skies
    #add vars for tree and grass density?
    app.happyColorDict = {'grass': ['#649e44', '#478f45', '#449642', '#298747'], 
                        'filter': app.happyFilter, "heightFac": 7, 
                        "grassSprite": app.grassSprite, 'density': 2}
    app.sadColorDict = {'grass': ['#4e6b5f', '#4e6b50', '#3e5e46', '#3f705e'], 
                        'filter': app.sadFilter, "heightFac": 1, 
                        "grassSprite": app.sadGrassSprite,  'density': 5}
    app.neutralColorDict = {'grass': ['#e0bb55', '#cf9c30', '#b3814d', '#d1893f'], 
                        'filter': app.neutralFilter, "heightFac": 5,
                        "grassSprite": app.neutralGrassSprite, 'density': 1}
    app.madColorDict = {'grass': ['#b56635', '#b54835', '#ad6b5f', '#c26936'], 
                        'filter': app.madFilter, "heightFac": 20,
                        "grassSprite": app.madGrassSprite, 'density': 10}

    if (app.vibe == "happy"):
        app.vibe = app.happyColorDict
    elif (app.vibe == "sad"):
        app.vibe = app.sadColorDict
    elif (app.vibe == "neutral"):
        app.vibe = app.neutralColorDict
    else:
        app.vibe = app.madColorDict
        
    #vars related to perlin noise
    app.perlinRows = 50
    app.perlinCols = app.perlinRows
    app.gradBoard = [[(0, 0)] * app.perlinRows for row in range(app.perlinRows)]
    app.perlinCellSize = 5 
    app.perlinBoardLength = 50
    app.perlinBoard = [[0] * app.perlinBoardLength 
                        for row in range(app.perlinBoardLength)]
    app.newPerlinBoard = [[0] * (app.perlinBoardLength* 2) 
                            for row in range(app.perlinBoardLength * 2)]
    app.newPerlinLength = app.perlinBoardLength * 2
    #stores color of perlin board 
    app.perlinColor = copy.deepcopy(app.newPerlinBoard)
    app.oct3PerlinBoard = [[0] * (app.perlinBoardLength//2) 
                            for row in range(app.perlinBoardLength//2)]
    app.oct3PerlinLength = app.perlinBoardLength//2

    calcGradVec(app, app.gradBoard)
    fillPerlinBoard(app)
    perlinOctave2(app)
    perlinOctave3(app)
    fillPerlin(app)

    #todo: optimization for perlin noise: convert everything into an image
    #and just have it scroll up
    
    gameMode_fillBoard(app, app.vibe['grass'])
    gameMode_fillGrassAndTrees(app)

    # gameMode_fillTrees(app)

#tree class
class Tree():
    def __init__(self, loc):
        self.loc = loc[0], loc[1]

    def playerIsNear(self, app):
        pX, pY = app.playerPos
        pass

class AppleTree(Tree):
    def __init__(self, loc):
        super().__init__()
        self.apples = 3
    
    def pickApples(self):
        if (self.apples == 0):
            return 0
        self.apples -= 1
        return self.apples



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
    newX = (x - y)/2 - 300
    newY = (x + y)/4 - 300
    return newX, newY

def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

#Checks for player movement
def gameMode_constraintsMet(app, r, c):
    return (r >= 0 and r < len(app.board) and c >= 0 and c < len(app.board[0]))

#To be implemented
def gameMode_expandBoard(app, dir):
    row, col = app.playerPos

def gameMode_mousePressed(app, event):
    if (app.displayJournal):
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayJournal = False
            #once done with reading journal, change into writing mode
            app.journal = open("journal.txt", "a+")
    if (0 <= event.x <= 100 and 0 <= event.y <= 100):
        app.displayJournal = True 
        if (app. displayJournal):
            app.journal.close()
            #change it into reading mode to display text
            app.journal = open("journal.txt", "r")

def gameMode_keyPressed(app, event):
    cx, cy = app.playerPos
    #Journal input
    if (app.goHome):
        if (event.key == "y"):
            app.goHome = False
            changeDate = open("date.txt", "w+")
            if (app.month == 12):
                app.month = 1
            if (app.day == 30):
                app.day = 1
                app.month += 1
            else:
                app.day += 1
            #update day for "next day"
            changeDate.write(f"{app.month}/{app.day}")
            changeDate.close()
            app.text = ""
            detectWords(app)
            appStarted(app)
    #how do i chceck if length of text is greater than smthn
    if (app.textLenChecker >= 20):
        app.textLenChecker = 0
        app.text += "\n"
    if (len(event.key) == 1):
        app.text += event.key
        app.textLenChecker += 1
        app.displayJournal = False 
    if (app.journal.mode != "r"):
        if (event.key == "Space"):
            app.text += " "
            app.textLenChecker += 1
        if (event.key == "Backspace"):
            app.text = app.text[:-1]
            app.textLenChecker -= 1
        if (app.text.lower() == "go home"):
            app.text = ""
            app.goHome = True
        if (event.key == 'Enter'):
            app.journal.write(app.text + "\n")
            app.text = ""
            app.textLenChecker += 1

    #Player movement
    if (event.key == 'Up'):
        # if (gameMode_constraintsMet(app, cx - app.speed, cy - app.speed)):
        # app.prevY += 40
        app.playerPos = (cx, cy - app.speed)
    elif (event.key == 'Down'):
        # if (gameMode_constraintsMet(app, cx + app.speed, cy + app.speed)):
        # app.prevY -= 40
        app.playerPos = (cx, cy + app.speed)
    elif (event.key == 'Right'):
        app.playerPos = (cx + app.speed, cy)
        app.playerDir = "right"
    elif (event.key == 'Left'):
        app.playerPos = (cx - app.speed, cy)

def getCellBoundsinCartesianCoords(app, row, col):
    x0 = col * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    return x0, y0, x1, y1

def getRowCol(app, x, y):
    row = (y - app.margin)//app.cellSize
    col = (x - app.margin)/app.cellSize
    return row, col

def findDate(date):
    separator = date.find("/")
    return int(date[:separator]), int(date[separator + 1:])

#Currently broken but too lazy to fix
def moveClouds(app):
    #Moves clouds dx + 1, dy - 1 per 1 sec, loops them
    tempBoard = copy.deepcopy(app.perlinColor)
    length = len(app.newPerlinBoard)
    for pX in range(0, length):
        for pY in range(0, length):
            if (pX == 0 or pY == length - 1):
                newColor = app.perlinColor[0][0]
            else:
                newColor = app.perlinColor[pX - 1][pY + 1]
            tempBoard[pX][pY] = newColor
    app.perlinColor = tempBoard

def gameMode_timerFired(app):
    moveClouds(app)
    app.timeSinceLastCloud += 1
    # if (app.timeSinceLastCloud >= 80):
    #     fillPerlin(app)
    #     app.timeSinceLastCloud = 0



#---------------------------------------
# JOURNAL FUNCTIONS
# --------------------------------------
def detectWords(app):
    #I should make lists for each of these words
    #takes in singular lines and checks for "words"
    app.journal.seek(0)
    lines = app.journal.readlines()
    for line in lines:
        #get entire text from entry
        if ("happy" in line or "good" in line):
            app.feelingsDict["happy"] = app.feelingsDict.get("happy", 0) + 1
        if ("sad" in line or "down" in line or "cry" in line):
            app.feelingsDict["sad"] = app.feelingsDict.get("sad", 0) + 1
        if ("meh" in line or "thinking" in line or "lonely" in line or "know" in line):
            app.feelingsDict["neutral"] = app.feelingsDict.get("neutral", 0) + 1
        if ("mad" in line or "angry" in line):
            app.feelingsDict["angry"] = app.feelingsDict.get("angry", 0) + 1
    changeColors(app)

def changeColors(app):
    largestMood = "happy"
    largestMoodCount = 0
    for feeling in app.feelingsDict:
        print(feeling, app.feelingsDict[feeling])
        if app.feelingsDict[feeling] > largestMoodCount:
            largestMood = feeling
            largestMoodCount = app.feelingsDict[feeling]
    changeFeeling = open("feeling.txt", "w+")
    changeFeeling.write(f"{largestMood}")
    changeFeeling.close()


#Fills board at beginning with colors, also called whenever new rows are added
def gameMode_fillBoard(app, colorBoard):
    #colorBoard is a list of colors corresponding to emotion
    #grassColorBoard is board that stores grass color
    print(colorBoard)
    rows, cols = len(app.grassColorBoard), len(app.grassColorBoard[0])
    for row in range(rows):
        for col in range(cols):
            if app.grassColorBoard[row][col] == 0:
                index = random.randint(0, len(colorBoard) - 1)
                app.grassColorBoard[row][col] = colorBoard[index]

def gameMode_fillGrassAndTrees(app):
    rows, cols = len(app.grassTreeBoard), len(app.grassTreeBoard )

#backtracking recursive function that makes words go onto the next line
#this deals with singular lines not the entire journal
def padWords(app, line):
    if (len(line) == 0):
        return 
    else:
        curLength = 0
        newLine = []
        while (curLength >= 30):
            wordList = line.split(" ")
            for i in range(len(wordList)):
                word = wordList[i]
                curLength += len(word)
                newLine.append(word)
                if (curLength >= 30):
                    #im too lazy tro do this lmao
                    return newLine + padWords(app, line)


def moveCamera(app, dx, dy):
    #imma need a TA to explain this one..
    pass

#---------------------------------------
# DRAW FUNCTIONS
# --------------------------------------

#Draws terrain according to height
def gameMode_drawCell(app, canvas, row, col, color):
    x0 = col * app.cellSize + app.margin
    y0 = row * app.cellSize + app.margin
    x1 = (col + 1) * app.cellSize + app.margin
    y1 = (row + 1) * app.cellSize + app.margin
    if (0 <= x0 <= app.width * 3 or 0 <= y0 <= app.height * 3):
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
        heightFac = app.vibe["heightFac"]
        yOffsetTopL = app.board[row][col] * heightFac
        if (row + 1 < app.rows):
            yOffsetBotL = app.board[row + 1][col] * heightFac
        else:
            yOffsetBotL = yOffsetTopL
        
        if (col + 1 < app.cols):
            yOffsetTopR = app.board[row][col + 1] * heightFac
        else:
            yOffsetTopR = yOffsetTopL
        
        if (row + 1 < app.rows and col + 1 < app.cols):
            yOffsetBotR = app.board[row + 1][col + 1] * heightFac
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
        # canvas.create_line(topX, topY, topX, topY - yOffsetBotL, width = 2)
        # canvas.create_line(rightX, rightY, rightX, rightY - yOffsetBotR, width = 2)
        # canvas.create_line(leftX, leftY, leftX, leftY - yOffsetTopL, width = 2)
        # canvas.create_line(botX, botY, botX, botY - yOffsetTopR, width = 2)
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

        # canvas.create_line(topX, topY, rightX, rightY, width = 2)
        # canvas.create_line(rightX, rightY, botX, botY, width = 2)
        # canvas.create_line(leftX, leftY, botX, botY, width = 2)
        # canvas.create_line(leftX, leftY, topX, topY, width = 2)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        # if (color == app.happyColor[1] or color == app.happyColor[0] or color == app.happyColor[2]):
        colorList = app.vibe["grass"]
        if (color != colorList[0]):
            grass = app.vibe["grassSprite"]
            grass = getCachedPhotoImage(app, grass)
            canvas.create_image(cx, cy - yOffsetTopL, image=grass)
        else:
            tree = getCachedPhotoImage(app, app.treeSprite)
            canvas.create_image(cx, cy - yOffsetTopL - 40, image=tree)

def fillPerlin(app):
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = app.newPerlinBoard[pX][pY]
            val2 = app.perlinBoard[pX//2][pY//2]
            val3 = app.oct3PerlinBoard[pX//4][pY//4]
            if (app.vibe == app.madColorDict):
                val = val #very small, kinda dotty clouds
            elif (app.vibe == app.sadColorDict):
                val = val3 #blocky, less clouds
            elif (app.vibe == app.neutralColorDict):
                val = val3 + val2 * 0.5 #slightly more normal looking clouds
            else:
                val = (val * 0.5) + (val2 * 0.5) + val3 #normal clouds!
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
            app.perlinColor[pX][pY] = color
            # color = rgb_color((val, val, val))

def gameMode_drawClouds(app, canvas):
    #Goes from 0 to 100
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            offset = app.width // app.newPerlinLength
            color = app.perlinColor[pX][pY]
            if (color != "#7ab7f0" and color != "#deecfc" and color != "#dae8f0"):
                    canvas.create_rectangle(pX * offset - offset, pY * offset - offset, 
                                    pX * offset + offset, pY * offset + offset, 
                                    fill = color, width = 0)


def gameMode_drawPlayer(app, canvas):
    # row, col = app.playerPos
    # x = col * app.cellSize
    # y = row * app.cellSize
    # yOffset = app.board[row][col] * heightFac
    x, y = app.playerPos
    # x, y = gameMode_2DToIso(app, x, y)
    # y += app.cellSize//2
    player = getCachedPhotoImage(app, app.playerSprite)
    canvas.create_image(x, y, image = player)
    # row, col = getRowCol(app, x, y)
    #i dont know how to get the player to appear in front of the tree...
    # if (app.grassColorBoard[row][col] == app.happyColor[0]):
    #     tree = getCachedPhotoImage(app, app.treeSprite)

    #     cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    #     cx, cy = gameMode_2DToIso(app, cx, cy)
    #     canvas.create_image(cx, cy - yOffsetTopL - 128, image=tree)


def gameMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    canvas.create_text(app.width/2, app.height/2, 
                        text = "you went home for the day and rested", 
                        fill = "white")
    canvas.create_text(app.width/2, app.height/2 + 20, 
                        text = "go out again the next morning? (y/n)",
                        fill = "white")

            

def gameMode_drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            gameMode_drawCell(app, canvas, row, col, app.grassColorBoard[row][col])
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
    filter = app.sadFilter
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    canvas.create_rectangle(50, 150, 750, 700, fill = "#f5eace")
    canvas.create_text(400, 220, text = "journal", 
                        font = "Courier 24 bold", anchor = "s")
    i = 0
    app.journal.seek(0)
    lines = app.journal.readlines()
    for line in lines:
        #recursive func that returns word so it isn't going too far on page
        # if (len(line) >= 30):
        #     textArr = padWords(line)
        if (i >= 25): 
            #put on next half of page
            canvas.create_text (600, 250 + (i - 25) * 20, text = line, font = "Courier 12 bold")
        else:
            canvas.create_text (200, 250 + i * 20, text = line, font = "Courier 12 bold")
        i += 1

    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)

    # for key in app.journal:
    #     canvas.create_text (200, 250 + i * 20, text = key)
    #     tex = app.journal[key]
    #     for entry in tex.splitlines():
    #         canvas.create_text(200, 250 + i * 20, text = entry)
    #         i += 1

def gameMode_drawTextAndUI(app, canvas):
    filter = app.vibe["filter"]
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    journalOpen = getCachedPhotoImage(app, app.journalOpenSprite)
    canvas.create_image(75, 75, image=journalOpen)
    canvas.create_text(app.width//2, 700, text = f"{app.text}", fill = "white",
                        font = "Courier 24 bold", anchor = "s")


def gameMode_drawGrass(app, canvas):
    # x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
    # cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
    # cx, cy = gameMode_2DToIso(app, cx, cy)
    # for _ in range(0, 3):
    #     cy -= app.board[row][col] * app.heightFac
    #     canvas.create_arc(cx - 20, cy - 20, cx, cy, style = CHORD, 
    #                         fill = "green", start = 110, width = 0)
    #     canvas.create_arc(cx , cy , cx + 20, cy + 20, style = CHORD, 
    #                     fill = "green", start = 120, width = 0)
    #     canvas.create_arc(cx - 10, cy - 10, cx + 10, cy + 10, style = CHORD, 
    #                         fill = "green", start = 150, width = 0)
    pass
    
#To be implemented 
def gameMode_drawTrees(app, canvas):
    pass

def gameMode_drawBackground(app, canvas):
    
    canvas.create_rectangle(0, 0, app.width, app.height, fill = f"#9bc7e8")



def gameMode_redrawAll(app, canvas):
    if (app.goHome):
        gameMode_drawHome(app, canvas)
    else:
        gameMode_drawBackground(app, canvas)
        gameMode_drawBoard(app, canvas) 
        gameMode_drawGrass(app, canvas)
        gameMode_drawTrees(app, canvas)
        gameMode_drawPlayer(app, canvas)
        gameMode_drawClouds(app, canvas)
        gameMode_drawTextAndUI(app, canvas)

    if (app.displayJournal):
        gameMode_drawJournal(app, canvas)

    # gameMode_drawObstacles(app, canvas)

runApp(width = 800, height = 800)