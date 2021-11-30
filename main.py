from cmu_112_graphics import *
import random
import pygame

'''
to-do
11/29 - finish UI for home, journal, inventory, recipe, inventory
11/30 - add sound and start + end screen + maybe sleep screen, 
        fancier lighting overlays
12/1 - add flowers and birds, misc bug fixes (in front/ behind trees),
        hills background
'''

#Credits: Code for drawBoard, constraintsMet, drawCell (first 10 lines)
# taken from code I wrote for hack112 
#2dToIso and IsoTo2D from: https://gamedevelopment.tutsplus.com/tutorials/creati
# ng-isometric-worlds-a-primer-for-game-developers--gamedev-6511
#Diamond square algorithm concept (not code) from: https://web.archive.org/web/2
# 0060420054134/http://www.gameprogrammer.com/fractal.html#diamond
#Perlin noise concept (not code) from https://web.archive.org/web/20170201233641
# /https://mzucker.github.io/html/perlin-noise-math-faq.html and 
#https://eev.ee/blog/2016/05/29/perlin-noise/
#getCachedPhotoImage from : https://www.cs.cmu.edu/~112/notes/notes-animations-p
# art4.html
#Code for opening / closing / writing / reading files adapted from : https://www
# .guru99.com/reading-and-writing-files-in-python.html
#and https://stackoverflow.com/questions/28873349/python-readlines-not-returning
# -anything
#Camera movement idea (not code) from PIL/Pillow mini 3d lecture
#https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=249eb6cc-06ee-450b-
# 8d1e-adda0085dd69

#Music by Louie Zong    
#east coast summer https://louiezong.bandcamp.com/track/east-coast-summer
#golden hour https://www.youtube.com/watch?v=FlAahnk74x4&ab_channel=LouieZong 
#acoustic dream https://www.youtube.com/watch?v=-vZSWGHrrgc&list=PLxQAFogMh4GWp
# m891zkN_4_w0QRJjglfY&index=49&ab_channel=LouieZong
#tides of summer https://louiezong.bandcamp.com/album/notes

#Sound class and code from https://www.cs.cmu.edu/~112/notes/notes-animations-pa
# rt4.html#playingSounds

#######################################

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()

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
    app.cellSize = 250
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
    app.board = diamondSquare(app, app.rows//2, app.board)

    #Gameplay variables
    app.timerCount = 0
    app.playerPos = (700, 100)
    app.playerSprite = 0
    app.spriteFactor = 1.5

    url = "playerFrontIdle.png"
    spritestrip = app.loadImage(url)
    app.frontIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.frontIdleSprite.append(sprite) #append each sprite to array


    url = "playerFrontWalk.png"
    spritestrip = app.loadImage(url)
    app.frontWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.frontWalkSprite.append(sprite) #append each sprite to array


    url = "playerLeftIdle.png"
    spritestrip = app.loadImage(url)
    app.leftIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.leftIdleSprite.append(sprite) #append each sprite to array

    url = "playerLeftWalk.png"
    spritestrip = app.loadImage(url)
    app.leftWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.leftWalkSprite.append(sprite) #append each sprite to array

    url = "playerBack.png"
    spritestrip = app.loadImage(url)
    app.backIdleSprite = []
    app.backWalkSprite = []
    for i in range(4):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        if (i <= 1):
            app.backIdleSprite.append(sprite) #append each sprite to array
        else:
            app.backWalkSprite.append(sprite)
            
    url = "playerRightIdle.png"
    spritestrip = app.loadImage(url)
    app.rightIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        app.rightIdleSprite.append(sprite) #append each sprite to array

    url = "playerRightWalk.png"
    spritestrip = app.loadImage(url)
    app.rightWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        app.rightWalkSprite.append(sprite) #append each sprite to array

    url = "player.png"
    app.playerHomeSprite = app.loadImage(url)

    app.playerSpriteCounter = 0
    app.lastPressedCounter = 0
    app.lastPressedKey = "left"
    app.playerSprite = app.leftIdleSprite #set to this by default
    app.speed = 50
    app.lives = 3
    app.score = 0
    app.gameOver = False
    app.brdWidth = 0
    app.playerDir = ""
    app.cameraOffset = 100
    app.boundingBoxLimit = 300
    app.prevX = 500
    app.prevY = 500
    app.skyColor = ["#6197ed"]
    app.timerDelay = 200
    app.timeSinceLastCloud = 0
    app.treeList = []
    app.behindTreeList = []
    app.frontTreeList = []
    app.font = "Forte"

    #INVENTORY VARS
    app.displayInventory = False
    app.inventoryDict = dict()
    app.inventoryGrid = [[0] * 7 for row in range(7)]
    app.inventoryOrder = []
    app.inventory = open("inventory.txt", "r")
    url = "inventory.png"
    app.inventorySprite = app.loadImage(url)
    app.inventorySprite = app.scaleImage(app.inventorySprite, 3)

    fillInventory(app) #fill inventory across days
    app.inventory.close()
    #REMINDER: have to have inventoryDict write to inventory file

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
    app.goBed = False
    app.displayRecipe = False
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
    app.journalOpenSprite = app.scaleImage(app.journalOpenSprite, 1)

    app.vibe = app.feeling.read() #reads 'happy", "sad", "neutral", or "anx"

    #RECIPES
    url = "tomatoandeggs.png"
    app.tomatoEggSprite = app.loadImage(url)
    app.tomatoEggSprite = app.scaleImage(app.tomatoEggSprite, 2)

    url = "applecake.png"
    app.appleCakeSprite = app.loadImage(url)
    app.appleCakeSprite = app.scaleImage(app.appleCakeSprite, 2)

    url = "dumplings.png"
    app.dumplingSprite = app.loadImage(url)
    app.dumplingSprite = app.scaleImage(app.dumplingSprite, 2)

    url = "peachcobbler.png"
    app.peachCobblerSprite = app.loadImage(url)
    app.peachCobblerSprite = app.scaleImage(app.peachCobblerSprite, 2)

    url = "porridge.png"
    app.porridgeSprite = app.loadImage(url)
    app.porridgeSprite = app.scaleImage(app.porridgeSprite, 2)

    url = "recipe.png"
    app.recipeSprite = app.loadImage(url)
    app.hungerMeter = random.randint(50, 100)
    app.recipeList = initializeRecipeList(app)
    url = "bed.png"
    app.bedSprite = app.loadImage(url)
    url = "recipeSprite.png"
    app.recipeIconSprite = app.loadImage(url)
    app.recipeIconSprite = app.scaleImage(app.recipeIconSprite, 3)


    #HOME VARS
    url = "room1.jpg"
    app.homeBackground = app.loadImage(url)
    app.homeBackground = app.scaleImage(app.homeBackground, 4)
    app.fridgeOrder = ["milk", "eggs", "meat", "tomatoes", "water"]
    app.fridgeItems = initializeItems(app, app.fridgeOrder)
    app.cabinetOrder = ["flour", "rice", "sugar", "soy sauce", "noodles"]
    app.cabinetItems = initializeItems(app, app.cabinetOrder)
    url = "home.png"
    app.homeSprite = app.loadImage(url)
    app.homeSprite = app.scaleImage(app.homeSprite, 3)

    app.homeX = 0
    app.homeCameraOffset = 40
    app.displayFridge = False
    app.displayCabinet = False
    app.displayStove = False
    app.fridgeLoc = (700, 400)
    app.cabinetLoc = (600, 400)
    app.stoveLoc = (300, 400)

    #Vars related to tree or nature stuff
    app.treeSpriteCounter = 0
    url = "tree.png"
    spritestrip = app.loadImage(url)
    app.treeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.9)
        app.treeSprite.append(sprite) #append each sprite to array

    url = "appletree.png"
    spritestrip = app.loadImage(url)
    app.appleTreeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.9)
        app.appleTreeSprite.append(sprite) #append each sprite to array
    

    url = "grass.png"
    app.grassSprite = app.loadImage(url)
    url = "neutralgrass.png"
    app.neutralGrassSprite = app.loadImage(url)
    url = "anxgrass.png"
    app.anxGrassSprite = app.loadImage(url)
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
    url = "anxFilter.png"
    app.anxFilter = app.loadImage(url)
    app.anxFilter = app.scaleImage(app.anxFilter, 4)


    #Color variations (for grass) to be implemented : color variations for
    #clouds, trees, skies
    app.happyColorDict = {'grass': ['#649e44', '#478f45', '#449642', '#298747'], 
                        'filter': app.happyFilter, "heightFac": 7, 
                        "grassSprite": app.grassSprite, 'density': 2}
    app.sadColorDict = {'grass': ['#4e6b5f', '#4e6b50', '#3e5e46', '#3f705e'], 
                        'filter': app.sadFilter, "heightFac": 1, 
                        "grassSprite": app.sadGrassSprite,  'density': 5}
    app.neutralColorDict = {'grass': ['#e0bb55', '#cf9c30', '#b3814d', 
                            '#d1893f'], 'filter': app.neutralFilter, 
                            "heightFac": 5, 
                            "grassSprite": app.neutralGrassSprite, 'density': 1}
    app.anxColorDict = {'grass': ['#b56635', '#b54835', '#ad6b5f', '#c26936'], 
                        'filter': app.anxFilter, "heightFac": 20,
                        "grassSprite": app.anxGrassSprite, 'density': 10}
    pygame.mixer.init()
    app.sound = ""
    if (app.vibe == "happy"):
        app.vibe = app.happyColorDict
        app.sound = Sound("summer.mp3")

    elif (app.vibe == "sad"):
        app.vibe = app.sadColorDict
        app.sound = Sound("acoustic dream.mp3")

    elif (app.vibe == "neutral"):
        app.vibe = app.neutralColorDict
        app.sound = Sound("the golden hour.mp3")
    else:
        app.vibe = app.anxColorDict
        app.sound = Sound("the golden hour.mp3")

    if (app.mode == "homeMode"):
        app.sound = Sound("tides of summer.mp3")


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
    
    gameMode_fillBoard(app, app.vibe['grass'], app.grassColorBoard)
    changeTreeList(app)
    
    # app.sound.start(loops = -1)

class Recipe():
    def __init__(self, name, requiredIngredients, sprite):
        self.name = name
        self.ingredients = requiredIngredients
        self.loc = (0, 0)
        self.sprite = sprite

class Item():
    def __init__(self, row, col, name):
        self.loc = (row, col)
        self.name = name
    
class Tree():
    def __init__(self, app, row, col):
        self.loc = (row, col)
        self.sprite = app.treeSprite


class AppleTree(Tree):
    def __init__(self, app, row, col):
        super().__init__(app, row, col)
        self.applesPicked = False
        self.sprite = app.appleTreeSprite

    def changeTree(self, app):
        if (self.applesPicked):
            self.sprite = app.treeSprite


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

#Credits see top
def gameMode_2DToIso(app, x, y):
    newX = (x - y)/2 - app.prevX
    newY = (x + y)/4 - app.prevY
    return newX, newY

def gameMode_IsoTo2D(app, x, y):
    newX = ((x + app.prevX) + 2 * (y + app.prevY))
    newY = (2 * (y + app.prevY) - (x + app.prevX))
    return newX, newY

def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

def getPlayerRowCol(app, x, y):
    cartX, cartY = gameMode_IsoTo2D(app, x, y)
    r, c = cartY//app.cellSize, cartX//app.cellSize
    r, c = r + 1, c + 1
    return r, c


#returns true if player x, y is within row, col bounds
def gameMode_constraintsMet(app, x, y):
    row, col = getPlayerRowCol(app, x, y)
    
    return (1 <= row <= app.rows and 1 <= col <= app.cols)

#If player is near edge of board, run diamond square on a new board
#and append it to old one
def gameMode_expandBoard(app):
    playerX, playerY = app.playerPos
    r, c = getPlayerRowCol(app, playerX, playerY)
    newBoard = createNewDiamondSquare(app)
    if (c >= app.cols - 3): #expand cols
        actualNewBoard = [[0] * (app.cols + 33) for row in range(app.rows)]
        newGrassBoard = copy.deepcopy(actualNewBoard)
        #want to attach first chunk
        bigChunk = [[0] * 33 for row in range(app.rows)]
        for chunk in range((app.rows//33)):
            newBoard = createNewDiamondSquare(app)
            newBoard = diamondSquare(app, 16, newBoard)
            for row in range(33 * chunk, 33 * (chunk + 1)):
                for col in range(33): #ex for first one goes from 0 to 33
                    bigChunk[row][col] = newBoard[row - (33 * chunk)][col]
        for row in range(app.rows):
            for col in range(app.cols + 33):
                if (col < app.cols):
                    actualNewBoard[row][col] = app.board[row][col]
                    newGrassBoard[row][col] = app.grassColorBoard[row][col]
                elif (col >= app.cols): #go from row to app.cols
                    actualNewBoard[row][col] = bigChunk[row][col - app.cols]
        app.board = actualNewBoard
        app.grassColorBoard = newGrassBoard
        app.rows, app.cols = len(app.board), len(app.board[0])
        gameMode_fillBoard(app, app.vibe['grass'], app.grassColorBoard)
    elif (r >= app.rows - 3): #elif on far end
        actualNewBoard = [[0] * app.cols for row in range(app.rows + 33)]
        newGrassBoard = copy.deepcopy(actualNewBoard)
        #want to attach first chunk
        bigChunk = [[0] * app.cols for row in range(33)]
        for chunk in range((app.cols//33)):
            newBoard = createNewDiamondSquare(app)
            newBoard = diamondSquare(app, 16, newBoard)
            for row in range(33):
                for col in range(33 * chunk, 33 * (chunk + 1)): 
                    a = newBoard[row][col - (33 * chunk)]
                    bigChunk[row][col] = a
        for row in range(app.rows + 33):
            for col in range(app.cols):
                if (row < app.rows):
                    actualNewBoard[row][col] = app.board[row][col]
                    newGrassBoard[row][col] = app.grassColorBoard[row][col]
                elif (row >= app.rows): 
                    actualNewBoard[row][col] = bigChunk[row - app.rows][col]
        app.board = actualNewBoard
        app.grassColorBoard = newGrassBoard
        app.rows, app.cols = len(app.board), len(app.board[0])
        gameMode_fillBoard(app, app.vibe['grass'], app.grassColorBoard)

#returns true if clicked on within item bounds
def withinRange(app, event, other):
    return (abs(event.x - other[0]) <= 30 and abs(event.y - other[1]) <= 30)

def homeMode_mousePressed(app, event):
    #open cabinet - stores flour, salt, sugar
    #open fridge - stores egg, milk
    #cook things in oven
    if (withinRange(app, event, app.stoveLoc)):
        app.displayStove = True
    if (withinRange(app, event, app.fridgeLoc)):
        app.displayFridge = True
    if (withinRange(app, event, app.cabinetLoc)):
        app.displayCabinet = True
    
    if (100 <= event.x <= 200 and 0 <= event.y <= 100):
        app.displayRecipe = not app.displayRecipe

    if (650 <= event.x <= 750 and 0 <= event.y <= 100):
        app.displayInventory = not app.displayInventory\

    if (350 <= event.x <= 450 and 600 <= event.y <= 750):
        app.goBed = True

    if app.displayFridge:
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayFridge = False
        for item in app.fridgeItems:
            if withinRange(app, event, item.loc):
                app.inventoryDict[item.name] = app.inventoryDict.get(item.name, 0) + 1
                if (item.name not in app.inventoryOrder):
                    app.inventoryOrder.append(item.name)

    if app.displayCabinet:
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayCabinet = False
        for item in app.cabinetItems:
            if withinRange(app, event, item.loc):
                app.inventoryDict[item.name] = app.inventoryDict.get(item.name, 0) + 1
                if (item.name not in app.inventoryOrder):
                    app.inventoryOrder.append(item.name)

    if app.displayStove:
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayStove = False
        canCook = True
        for recipe in app.recipeList:
            if withinRange(app, event, recipe.loc):
                recipeDict = recipe.ingredients
                for ingredient in recipeDict:
                    if ingredient not in app.inventoryDict or app.inventoryDict[ingredient] < recipeDict[ingredient]:
                        print("insufficient ingredients")
                        canCook = False
                if (canCook):
                    for ingredient in recipeDict:
                        app.inventoryDict[ingredient] -= recipeDict[ingredient]
                        #remove used ingredients
                    print("cooked recipe")
                    app.inventoryDict[recipe.name] = app.inventoryDict.get(recipe.name, 0) + 1
                    app.inventoryOrder.append(recipe.name)

def gameMode_mousePressed(app, event):
    if (app.displayJournal):
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayJournal = False
            #once done with reading journal, change into writing mode
            app.journal = open("journal.txt", "a+")
    elif (0 <= event.x <= 100 and 0 <= event.y <= 100):
        app.displayJournal = True 
        if (app. displayJournal):
            app.journal.close()
            #change it into reading mode to display text
            app.journal = open("journal.txt", "r")
    elif (150 <= event.x <= 200 and 0 <= event.y <= 100):
        app.displayRecipe = True
    elif (app.displayRecipe):
        if (50 <= event.x <= 150 and 150 <= event.y <= 250):
            app.displayRecipe = False
    elif (650 <= event.x <= 750 and 0 <= event.y <= 100):
        app.displayInventory = not app.displayInventory
    else:
        cx, cy = app.playerPos
        playerRow, playerCol = getPlayerRowCol(app, cx, cy)
        for tree in app.treeList:
            row, col = tree.loc
            if (abs(row - playerRow) <= 2 and abs(col - playerCol) <= 2 and type(tree) == AppleTree):
                if not (tree.applesPicked):
                    tree.applesPicked = True
                    tree.changeTree(app)
                    app.inventoryDict["apples"] = app.inventoryDict.get("apples", 0) + 3
                    if ("apples" not in app.inventoryOrder):
                        app.inventoryOrder.append("apples")
                    # print(tree.loc)
                    break   

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

def homeMode_moveCamera(app, dir):
    x, y = app.playerPos
    if (dir == "left"):
        if (x <= app.boundingBoxLimit):
            app.homeX -= app.homeCameraOffset
            app.stoveLoc = (app.stoveLoc[0] + app.homeCameraOffset, app.stoveLoc[1])
            app.fridgeLoc = (app.fridgeLoc[0] + app.homeCameraOffset, app.fridgeLoc[1])
            app.cabinetLoc = (app.cabinetLoc[0] + app.homeCameraOffset, app.cabinetLoc[1])

    elif (dir == "right"):
        if (x >= app.width - app.boundingBoxLimit):
            app.homeX += app.homeCameraOffset
            app.stoveLoc = (app.stoveLoc[0] - app.homeCameraOffset, app.stoveLoc[1])
            app.fridgeLoc = (app.fridgeLoc[0] - app.homeCameraOffset, app.fridgeLoc[1])
            app.cabinetLoc = (app.cabinetLoc[0] - app.homeCameraOffset, app.cabinetLoc[1])

def homeMode_keyPressed(app, event):
    cx, cy = app.playerPos
    if (app.goBed):
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

    if (event.key == 'Right'):
            app.playerPos = (cx + app.speed, cy)
            homeMode_moveCamera(app, "right")
    if (event.key == 'Left'):
            app.playerPos = (cx - app.speed, cy)
            homeMode_moveCamera(app, "left")

def gameMode_keyPressed(app, event):
    cx, cy = app.playerPos
    #Journal input
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
            app.playerPos = (400, 600)
            # update vars for home
            app.playerSprite = app.scaleImage(app.playerHomeSprite, 3.5)
            app.goHome = True
            app.sound = Sound("tides of summer.mp3")
            app.sound.start(loops = -1)
            app.mode = "homeMode"
        if (event.key == 'Enter'):
            app.journal.write(app.text + "\n")
            app.text = ""
            app.textLenChecker += 1

    #Player movement
    if (event.key == 'Up'):
        if gameMode_constraintsMet(app, cx, cy - app.speed):
            app.playerPos = (cx, cy - app.speed)
            app.playerSprite = app.backWalkSprite
            gameMode_moveCamera(app, "up")
    elif (event.key == 'Down'):
        if gameMode_constraintsMet(app, cx, cy + app.speed):
            app.playerPos = (cx, cy + app.speed)
            app.playerSprite = app.frontWalkSprite
            gameMode_moveCamera(app, "down")
    elif (event.key == 'Right'):
        if gameMode_constraintsMet(app, cx + app.speed, cy):
            app.playerPos = (cx + app.speed, cy)
            app.playerSprite = app.rightWalkSprite
            gameMode_moveCamera(app, "right")
    elif (event.key == 'Left'):
        if gameMode_constraintsMet(app, cx - app.speed, cy):
            app.playerPos = (cx - app.speed, cy)
            app.playerSprite = app.leftWalkSprite
            gameMode_moveCamera(app, "left")
    
    if (event.key == 'Up' or event.key == 'Down' or event.key == 'Right' or
        event.key == 'Left'):
        changeTreeList(app)
        gameMode_expandBoard(app)

def gameMode_keyReleased(app, event):
    if (event.key == 'Up'):
        app.lastPressedKey = "Up"
    elif (event.key == 'Down'):
        app.lastPressedKey = "Down"
    elif (event.key == 'Right'):
        app.lastPressedKey = "Right"
    elif (event.key == 'Left'):
        app.lastPressedKey = "Left"   

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

def fillInventory(app):
    inventorylines = app.inventory.read() #will return array of lines
    for line in inventorylines:  #ex apples 3
        entry = line.split(" ") #splits into array [apples, 3]
        item = entry[0]
        number = entry[1] 
        app.inventory[item] = number
        if item not in app.inventoryOrder:
            app.inventoryOrder.append(item) #inventoryOrder is just,,, 

#Returns date
def findDate(date):
    separator = date.find("/")
    return int(date[:separator]), int(date[separator + 1:])

def initializeItems(app, L):
    newL = []
    for i in range(len(L)):
        newL.append(Item(0, i, L[i]))
    return newL

def initializeRecipeList(app):
    newL = []
    newL.append(Recipe("tomato and eggs", {"tomatoes" : 2, "eggs" : 3, "rice": 1},
                        app.tomatoEggSprite))
    newL.append(Recipe("meat and fennel dumplings", {"meat" : 2, "fennel" : 3, "flour" : 2},
                        app.dumplingSprite))
    newL.append(Recipe("porridge", {"rice" : 3, "water" : 3, "eggs" : 2, "scallions" : 2},
                        app.porridgeSprite))
    newL.append(Recipe("apple cake", {"flour" : 2, "apples" : 2, "eggs" : 2, "water" : 2},
                        app.appleCakeSprite))
    newL.append(Recipe("peach cobbler", {"peaches" : 3, "flour" : 2, "eggs" : 1, "water" : 1},
                        app.peachCobblerSprite))
    return newL

#Moves clouds
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

def changeTreeList(app):
    playerX, playerY = app.playerPos
    for i in range(len(app.treeList)):
        tree = app.treeList[i]
        row, col = tree.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        cy -= 120
        if (cy <= playerY + 42): #tree is behind player
            app.behindTreeList.append(tree)
            if (tree in app.frontTreeList):
                app.frontTreeList.remove(tree)
        elif (cy >= playerY - 42): #tree is in front of player
            app.frontTreeList.append(tree)
            if (tree in app.behindTreeList):
                app.behindTreeList.remove(tree)

def gameMode_timerFired(app):
    moveClouds(app)
    app.timeSinceLastCloud += 1
    # if (app.timeSinceLastCloud >= 80):
    #     fillPerlin(app)
    #     app.timeSinceLastCloud = 0
    app.hungerMeter -= 0.2
    app.playerSpriteCounter = (1 + app.playerSpriteCounter) % len(app.playerSprite)
    app.treeSpriteCounter = (1 + app.treeSpriteCounter) % len(app.treeSprite)
    app.lastPressedCounter += 1
    if (app.lastPressedCounter >= 1):
        if (app.lastPressedKey == 'Up'):
            app.playerSprite = app.backIdleSprite
        elif (app.lastPressedKey == 'Down'):
            app.playerSprite = app.frontIdleSprite
        elif (app.lastPressedKey == 'Right'):
            app.playerSprite = app.rightIdleSprite
        elif (app.lastPressedKey == 'Left'):
            app.playerSprite = app.leftIdleSprite   
        app.lastPressedCounter = 0
#---------------------------------------
# JOURNAL FUNCTIONS
# --------------------------------------
def detectWords(app):
    app.journal.seek(0)
    lines = app.journal.readlines()
    for line in lines:
        #get entire text from entry
        if ("happy" in line or "good" in line):
            app.feelingsDict["happy"] = app.feelingsDict.get("happy", 0) + 1
        if ("sad" in line or "down" in line or "cry" in line):
            app.feelingsDict["sad"] = app.feelingsDict.get("sad", 0) + 1
        if ("lonely" in line or "thinking" in line or "know" in line):
            app.feelingsDict["neutral"] = app.feelingsDict.get("neutral", 0) + 1
        if ("mad" in line or "mad" in line or "anxious" in line):
            app.feelingsDict["anx"] = app.feelingsDict.get("anx", 0) + 1
    changeColors(app)

def changeColors(app):
    largestMood = "happy"
    largestMoodCount = 0
    for feeling in app.feelingsDict:
        # print(feeling, app.feelingsDict[feeling])
        if app.feelingsDict[feeling] > largestMoodCount:
            largestMood = feeling
            largestMoodCount = app.feelingsDict[feeling]
    changeFeeling = open("feeling.txt", "w+")
    changeFeeling.write(f"{largestMood}")
    changeFeeling.close()


#Fills board at beginning with colors, also called whenever new rows are added
def gameMode_fillBoard(app, colorBoard, grassBoard):
    #colorBoard is a list of colors corresponding to emotion
    #grassColorBoard is board that stores grass color
    rows, cols = len(grassBoard), len(grassBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (grassBoard[row][col] == 0):
                index = random.randint(0, len(colorBoard) - 1)
                grassBoard[row][col] = colorBoard[index]
            #add tree location
            for tree in app.treeList:
                if (tree.loc == (row, col)):
                    break
            if (grassBoard[row][col] == colorBoard[2]):
                chance = random.randint(1, 2)
                if (chance == 1):
                    app.treeList.append(Tree(app, row, col))
                else:
                    app.treeList.append(AppleTree(app, row, col))

#function that adds new pages
def makeNewPages(app, line):
    #to be implemented
    pass

def gameMode_moveCamera(app, dir):
    #if player is a certain amount of distance away from the screen
    x, y = app.playerPos
    if (dir == "left"):
        if (x <= app.boundingBoxLimit):
            app.prevX -= app.cameraOffset
    elif (dir == "right"):
        if (x >= app.width - app.boundingBoxLimit):
            app.prevX += app.cameraOffset
    elif (dir == "up"):
        if (y <= app.boundingBoxLimit):
            app.prevY -= app.cameraOffset
    elif (dir == "down"): 
        if (y >= app.height - app.boundingBoxLimit):
            app.prevY += app.cameraOffset

#---------------------------------------
# DRAW FUNCTIONS
# --------------------------------------

#Draws terrain according to height
def gameMode_drawCell(app, canvas, row, col, color):
    x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
    leftX, leftY = gameMode_2DToIso(app, x0, y0)
    if (0 <= leftX <= app.width or 0 <= leftY <= app.height):
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
            try:
                yOffsetBotR = app.board[row + 1][col + 1] * heightFac
            except:
                print(row, col)

        else:
            yOffsetBotR = yOffsetTopL

        #Draws sides
        canvas.create_polygon(leftX, leftY, leftX, leftY - yOffsetTopL, 
                            botX, botY - yOffsetTopR, botX, botY, fill = color )
        canvas.create_polygon(botX, botY, botX, botY - yOffsetTopR, 
                                rightX, rightY - yOffsetTopL, rightX, rightY, 
                                fill = color )
        canvas.create_polygon(botX, botY, botX, botY - yOffsetTopR, 
                                topX, topY - yOffsetBotL, topX, topY, 
                                fill = color )
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
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        colorList = app.vibe["grass"]
        if (color == colorList[1]):
            grass = app.vibe["grassSprite"]
            grass = getCachedPhotoImage(app, grass)
            canvas.create_image(cx, cy - yOffsetTopL, image=grass)
        


def fillPerlin(app):
    for pX in range(0, app.newPerlinLength):
        for pY in range(0, app.newPerlinLength):
            val = app.newPerlinBoard[pX][pY]
            val2 = app.perlinBoard[pX//2][pY//2]
            val3 = app.oct3PerlinBoard[pX//4][pY//4]
            if (app.vibe == app.anxColorDict):
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
            if(color!= "#7ab7f0" and color != "#deecfc" and color != "#dae8f0"):
                    canvas.create_rectangle(pX * offset - offset, 
                                    pY * offset - offset, 
                                    pX * offset + offset, pY * offset + offset, 
                                    fill = color, width = 0)

def gameMode_drawRecipeBook(app, canvas):
    filter = app.sadFilter
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    i = 0
    startX = 200
    xOffset = 400
    for recipe in app.recipeList:
        if (i >= 12):
            #draw on other half of screen
            canvas.create_text(startX + xOffset, startX + (i - 12) * 30, text = recipe.name, 
                font = f"{app.font} 12 bold")
            img = getCachedPhotoImage(app, recipe.sprite)
            canvas.create_image(startX + xOffset + 100, startX + (i - 12) * 30, image=img)
            for item in recipe.ingredients:
                i += 1
                canvas.create_text(startX + xOffset, startX + (i - 12) * 30, text = f"{item} : {recipe.ingredients[item]}",
                font = f"{app.font} 12 bold")
            i += 1
        else: 
            #draw on first half of screen
            canvas.create_text(startX, startX + i * 30, text = recipe.name, 
                font = f"{app.font} 12 bold")
            img = getCachedPhotoImage(app, recipe.sprite)
            canvas.create_image(startX + 100, startX + i * 30, image=img)
            for item in recipe.ingredients:
                i += 1
                canvas.create_text(startX, startX + i * 30, text = f"{item} : {recipe.ingredients[item]}",
                font = f"{app.font} 12 bold")
            i += 1
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)


def gameMode_drawInventory(app, canvas):
    rows, cols = len(app.inventoryGrid), len(app.inventoryGrid[0])
    inventoryIndex = 0
    for row in range(rows):
        for col in range(cols):
            x0 = col * 100 + app.margin
            x1 = (col + 1) * 100 + app.margin
            y0 = row * 100 + app.margin
            y1 = (row + 1) * 100 + app.margin
            if (2 <= row <= 5 and 2 <= col <= 5):
                canvas.create_rectangle(x0, y0, x1, y1, fill = "white")
                if (inventoryIndex < len(app.inventoryOrder)):
                    item = app.inventoryOrder[inventoryIndex]
                    canvas.create_text(x0, y0, text = f"{item} : {app.inventoryDict[item]}")
                    inventoryIndex += 1

def gameMode_drawPlayer(app, canvas):
    x, y = app.playerPos
    player = getCachedPhotoImage(app, app.playerSprite[app.playerSpriteCounter])
    canvas.create_image(x, y, image = player)

def homeMode_drawPlayer(app, canvas):
    x, y = app.playerPos
    player = getCachedPhotoImage(app, app.playerSprite)
    canvas.create_image(x, y, image = player)


def gameMode_drawBoard(app, canvas):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        for col in range(cols):
            gameMode_drawCell(app, canvas, row, col, 
                                app.grassColorBoard[row][col])


def gameMode_drawJournal(app, canvas):
    filter = app.sadFilter
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    canvas.create_rectangle(50, 150, 750, 700, fill = "#f5eace")
    canvas.create_text(400, 220, text = "journal", 
                        font = f"{app.font} 24 bold", anchor = "s")
    i = 0
    app.journal.seek(0)
    lines = app.journal.readlines()
    for line in lines:
        if (i >= 25): 
            #put on next half of page
            canvas.create_text (600, 250 + (i - 25) * 20, text = line, 
            font = f"{app.font} 12 bold")
        else:
            canvas.create_text (200, 250 + i * 20, text = line, 
            font = f"{app.font} 12 bold")
        i += 1

    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)

def gameMode_drawTextAndUI(app, canvas):
    filter = app.vibe["filter"]
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    journalOpen = getCachedPhotoImage(app, app.journalOpenSprite)
    canvas.create_image(75, 75, image=journalOpen)
    canvas.create_text(app.width//2, 700, text = f"{app.text}", fill = "white",
                        font = "Courier 24 bold", anchor = "s")
    recipeIcon = getCachedPhotoImage(app, app.recipeIconSprite)
    homeIcon = getCachedPhotoImage(app, app.homeSprite)
    inventoryIcon = getCachedPhotoImage(app, app.inventorySprite)

    canvas.create_image(200, 75, image=recipeIcon)
    canvas.create_image(700, 75, image=inventoryIcon)
    canvas.create_image(700, 700, image=homeIcon)

    # hungerStart = 500
    # canvas.create_rectangle(hungerStart, 600, hungerStart + 200, 650, fill = "black")
    # hungerPos = hungerStart + (app.hungerMeter/100) * 200
    # canvas.create_rectangle(hungerStart, 600, hungerPos, 650, fill = "red")


def gameMode_drawTreesInBack(app, canvas):
    for tree in app.behindTreeList:
        row, col = tree.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
            tree = getCachedPhotoImage(app, tree.sprite[app.treeSpriteCounter])
            canvas.create_image(cx, cy - 120, image=tree)


def gameMode_drawTreesInFront(app, canvas):
    for tree in app.frontTreeList:
        row, col = tree.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
            tree = getCachedPhotoImage(app, tree.sprite[app.treeSpriteCounter])
            canvas.create_image(cx, cy - 120, image=tree)


def gameMode_drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = f"#9bc7e8")

def homeMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    home = getCachedPhotoImage(app, app.homeBackground)
    canvas.create_image(400 - app.homeX, 400, image = home)
    x, y = app.stoveLoc
    canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill = "grey")
    x, y = app.fridgeLoc
    canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill = "white")
    x, y = app.cabinetLoc
    canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill = "brown")

def homeMode_drawBed(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    canvas.create_text(app.width/2, app.height/2, 
                        text = "you went to bed for the day", 
                        fill = "white")
    canvas.create_text(app.width/2, app.height/2 + 20, 
                        text = "go out again the next morning? (y/n)",
                        fill = "white")

def homeMode_drawStove(app, canvas):
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    i = 0
    for recipe in app.recipeList:
        canvas.create_text(200, 200 + i * 50, text = recipe.name)
        canvas.create_text(400, 200 + i * 50, text = recipe.ingredients)
        recipe.loc = (200, (200 + i * 50))
        i += 1
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)

def homeMode_drawCabinet(app, canvas):
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    for i in range(len(app.cabinetItems)):
        item = app.cabinetItems[i]
        canvas.create_text(200, 200 + i * 50, text = item.name)
        item.loc = (200, 200 + i * 50)
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)

def homeMode_drawFridge(app, canvas):
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    for i in range(len(app.fridgeItems)):
        item = app.fridgeItems[i]
        canvas.create_text(200, 200 + i * 50, text = item.name)
        item.loc = (200, 200 + i * 50)
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)

def homeMode_drawUI(app, canvas):
    if (app.displayCabinet):
        homeMode_drawCabinet(app, canvas)

    if (app.displayFridge): 
        homeMode_drawFridge(app, canvas)

    if (app.displayStove):
        homeMode_drawStove(app, canvas)

    if (app.displayInventory):
        gameMode_drawInventory(app, canvas)
    
    if (app.displayRecipe):
        gameMode_drawRecipeBook(app, canvas)

    journalOpen = getCachedPhotoImage(app, app.journalOpenSprite)
    canvas.create_image(700, 75, image=journalOpen) #inventory
    canvas.create_image(150, 75, image=journalOpen) #recipe 
    bed = getCachedPhotoImage(app, app.bedSprite)
    canvas.create_image(400, 650, image= bed) #inventory


def homeMode_redrawAll(app, canvas):
    if (app.goBed):
        homeMode_drawBed(app, canvas)
    else:
        homeMode_drawHome(app, canvas)
        homeMode_drawPlayer(app, canvas)
        homeMode_drawUI(app, canvas)

def gameMode_redrawAll(app, canvas):
    gameMode_drawBackground(app, canvas)
    gameMode_drawBoard(app, canvas) 
    gameMode_drawTreesInBack(app, canvas)
    gameMode_drawPlayer(app, canvas)
    gameMode_drawTreesInFront(app, canvas)
    gameMode_drawClouds(app, canvas)
    gameMode_drawTextAndUI(app, canvas)

    if (app.displayJournal):
        gameMode_drawJournal(app, canvas)

    if (app.displayRecipe):
        gameMode_drawRecipeBook(app, canvas)
    
    if (app.displayInventory):
        gameMode_drawInventory(app, canvas)

runApp(width = 800, height = 800) 