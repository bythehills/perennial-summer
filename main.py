from cmu_112_graphics import *
from classes import *
from perlin import *
from helper import *
from diamondsquare import *
import random
import pygame
import text2emotion as te


#Credits: Code for drawBoard, drawCell (first 10 lines)
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
#File import code from https://stackoverflow.com/questions/20309456/call-a-func
# tion-from-another-file

#Music by Louie Zong    
#east coast summer https://louiezong.bandcamp.com/track/east-coast-summer
#golden hour https://www.youtube.com/watch?v=FlAahnk74x4&ab_channel=LouieZong 
#acoustic dream https://www.youtube.com/watch?v=-vZSWGHrrgc&list=PLxQAFogMh4GWp
# m891zkN_4_w0QRJjglfY&index=49&ab_channel=LouieZong
#tides of summer https://louiezong.bandcamp.com/album/notes

#Sound class and code from https://www.cs.cmu.edu/~112/notes/notes-animations-pa
# rt4.html#playingSounds
#list of fonts from https://stackoverflow.com/questions/39614027/list-available-
# font-families-in-tkinter/47415907
# Channels code from https://stackoverflow.com/questions/53617967/play-music-and
# -sound-effects-on-top-of-each-other-pygame
#Sound effects created with https://sfxr.me/

#Sprite-related code (spritesheet, spritecounter, cropping, scaling) from:
#also scaling image code and screen mode code
#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

#Text to emotion module and code taken from
#https://towardsdatascience.com/text2emotion-python-package-to-detect-emotions-
# from-textual-data-b2e7b7ce1153
#and https://pypi.org/project/text2emotion/#description

#All art by me, inspiration taken from Animal Crossing (for trees)
#######################################

#Initialize vars
def appStarted(app):
    app.mode = "startScreen"
    #START SCREEN VARIABLES 
    app.startLoc = (300, 550)
    app.helpLoc = (500, 550)
    app.helpSprite = app.loadImage("art/helpSprite.png")
    app.helpSprite = app.scaleImage(app.helpSprite, 1.5)
    app.helpIcon = Icon("Help", (100, 700), app.helpSprite)
    app.isHelp = False
    app.isCheat = False #used to change game mood at end of day
    app.cheatMood = "happy"
    #press h for happy, l for neutral, a for anxious, s for sad

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

    spritestrip = app.loadImage("art/playerFrontIdle.png")
    app.frontIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.frontIdleSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage("art/playerFrontWalk.png")
    app.frontWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.frontWalkSprite.append(sprite) #append each sprite to array


    spritestrip = app.loadImage("art/playerLeftIdle.png")
    app.leftIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.leftIdleSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage("art/playerLeftWalk.png")
    app.leftWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)

        app.leftWalkSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage("art/playerBack.png")
    app.backIdleSprite = []
    app.backWalkSprite = []
    for i in range(4):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        if (i <= 1):
            app.backIdleSprite.append(sprite) #append each sprite to array
        else:
            app.backWalkSprite.append(sprite)
            
    spritestrip = app.loadImage("art/playerRightIdle.png")
    app.rightIdleSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        app.rightIdleSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage("art/playerRightWalk.png")
    app.rightWalkSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, app.spriteFactor)
        app.rightWalkSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage( "art/homePlayer.png")
    app.leftHomeIdleSprite = []
    app.rightHomeIdleSprite = []
    app.rightHomeWalkSprite = []
    app.leftHomeWalkSprite = []
    app.homeSpriteCounter = 0
    for i in range(4):
        sprite = spritestrip.crop((0, 64 * i, 64, 64 * (1 + i)))
        sprite = app.scaleImage(sprite, 4.5)
        if (i <= 1):
            app.leftHomeIdleSprite.append(sprite) #append each sprite to array
        else:
            app.leftHomeWalkSprite.append(sprite)
    for i in range(2):
        app.rightHomeWalkSprite.append(app.leftHomeWalkSprite[i].transpose(Image.FLIP_LEFT_RIGHT))
    for i in range(2):
        app.rightHomeIdleSprite.append(app.leftHomeIdleSprite[i].transpose(Image.FLIP_LEFT_RIGHT))

    app.playerHomeSprite = app.leftHomeIdleSprite

    app.playerSpriteCounter = 0
    app.lastPressedCounter = 0
    app.lastPressedKey = "left"
    app.playerSprite = app.leftIdleSprite #set to this by default
    app.speed = 30
    app.lives = 3
    app.score = 0
    app.brdWidth = 0
    app.playerDir = ""
    app.cameraOffset = 100
    app.boundingBoxLimit = 200
    app.prevX = 500
    app.prevY = 500
    app.skyColor = ["#6197ed"]
    app.timerDelay = 300
    app.treeList = []
    app.behindTreeList = []
    app.frontTreeList = []
    app.font = "Fixedsys"
    app.homeTextTimer = 3
    app.homeText = ""
    app.lastClickedLoc = (0, 0)

    #INVENTORY VARS
    app.displayInventory = False
    app.inventoryGrid = [[0] * 7 for row in range(7)]
    #this stores order in which to draw items
    app.inventoryList = []
    app.inventorySprite = app.loadImage("art/inventory.png")
    app.inventorySprite = app.scaleImage(app.inventorySprite, 3)
    app.inventoryIcon = Icon("Inventory", (700, 75), app.inventorySprite)


    #INITIALIZE ITEMS (This includes recipes)
    app.appleSprite = app.loadImage("art/apple.png")
    app.appleSprite = app.scaleImage(app.appleSprite, 1)
    app.appleItem = Item("apples", (0, 0), app.appleSprite, True)
    app.eggSprite = app.loadImage("art/eggs.png")
    app.eggSprite = app.scaleImage(app.eggSprite, 1)
    app.eggItem = Item("eggs", (0, 0), app.eggSprite, False)
    app.flourSprite = app.loadImage("art/flour.png")
    app.flourSprite = app.scaleImage(app.flourSprite, 1)
    app.flourItem = Item("flour", (0, 0), app.flourSprite, False)
    app.peachSprite = app.loadImage("art/peach.png")
    app.peachSprite = app.scaleImage(app.peachSprite, 1)
    app.peachItem = Item("peaches", (0, 0), app.peachSprite, True)
    app.noodleSprite = app.loadImage("art/noodles.png")
    app.noodleSprite = app.scaleImage(app.noodleSprite, 1)
    app.noodlesItem = Item("noodles", (0, 0), app.noodleSprite, False)
    app.riceSprite = app.loadImage("art/rice.png")
    app.riceSprite = app.scaleImage(app.riceSprite, 1)
    app.riceItem = Item("rice", (0, 0), app.riceSprite, False)
    app.waterSprite = app.loadImage("art/water.png")
    app.waterSprite = app.scaleImage(app.waterSprite, 1)
    app.waterItem = Item("water", (0, 0), app.waterSprite, True)
    app.tomatoSprite = app.loadImage("art/tomato.png")
    app.tomatoSprite = app.scaleImage(app.tomatoSprite, 1)
    app.tomatoItem = Item("tomatoes", (0, 0), app.tomatoSprite, True)
    app.soySauceSprite = app.loadImage("art/soy sauce.png")
    app.soySauceSprite = app.scaleImage(app.soySauceSprite, 1)
    app.soySauceItem = Item("soy sauce", (0, 0), app.soySauceSprite, False)
    app.sugarSprite = app.loadImage("art/sugar.png")
    app.sugarSprite = app.scaleImage(app.sugarSprite, 1)
    app.sugarItem = Item("sugar", (0, 0), app.sugarSprite, False)
    app.meatSprite = app.loadImage("art/meat.png")
    app.meatSprite = app.scaleImage(app.meatSprite, 1)
    app.meatItem = Item("meat", (0, 0), app.meatSprite, False)
    app.scallionSprite = app.loadImage("art/scallion.png")
    app.scallionSprite = app.scaleImage(app.scallionSprite, 1)
    app.scallionItem = Item("scallions", (0, 0), app.scallionSprite, False)
    app.fennelSprite = app.loadImage("art/fennel.png")
    app.fennelSprite = app.scaleImage(app.fennelSprite, 1)
    app.fennelItem = Item("fennel", (0, 0), app.fennelSprite, False)

    #JOURNAL VARS
    app.journal = open("journal.txt", "a+")
    app.journalDict = dict() #stores pages
    app.currentPage = 0
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
    app.goBedConfirm = False
    app.displayRecipe = False
    date = app.date.read()
    app.month, app.day = findDate(date)
    app.date.close()
    if (app.day != 1):
        app.mode = "gameMode"
    #when it starts u have to start w/ /6/1 on DATE.TXT, not JOURNAL.TXT
    #JOURNAL.TXT SHOULD BE EMPTY!!!
    #app.date updates with new day, write that day down
    app.journal.write(f"\n{app.month}/{app.day}\n") 
    app.journalOpenSprite = app.loadImage("art/journalopen.png")
    app.rightArrowSprite = app.scaleImage(app.loadImage("art/rightarrow.png"), 0.5)
    app.leftArrowSprite = app.rightArrowSprite.transpose(Image.FLIP_LEFT_RIGHT)
    app.rightArrowIcon = Icon("Right Arrow", (700, 600), app.rightArrowSprite)
    app.leftArrowIcon = Icon("Left Arrow", (100, 600), app.leftArrowSprite)

    app.journalCloseSprite = app.loadImage("art/journalclose.png")
    app.journalIcon = Icon("Journal", (75, 75), app.journalOpenSprite)
    app.closeIcon = Icon("Close", (75, 200), app.journalCloseSprite)

    app.vibe = app.feeling.read() #reads 'happy", "sad", "neutral", or "anx"

    #RECIPES
    app.tomatoEggSprite = app.loadImage("art/tomatoandeggs.png")
    app.tomatoEggSprite = app.scaleImage(app.tomatoEggSprite, 2)
    app.appleCakeSprite = app.loadImage("art/applecake.png")
    app.appleCakeSprite = app.scaleImage(app.appleCakeSprite, 2)
    app.dumplingSprite = app.loadImage("art/dumplings.png")
    app.dumplingSprite = app.scaleImage(app.dumplingSprite, 2)

    app.peachCobblerSprite = app.loadImage("art/peachcobbler.png")
    app.peachCobblerSprite = app.scaleImage(app.peachCobblerSprite, 2)

    app.porridgeSprite = app.loadImage("art/porridge.png")
    app.porridgeSprite = app.scaleImage(app.porridgeSprite, 2)

    app.scallionNoodlesSprite = app.loadImage("art/scallionnoodles.png")
    app.scallionNoodlesSprite = app.scaleImage(app.scallionNoodlesSprite, 2)
    
    #Initialize these as items as well....
    app.tomatoEggItem = Item("tomato and eggs", (0, 0), app.tomatoEggSprite,
                                True)
    app.appleCakeItem = Item("apple cake", (0, 0), app.appleCakeSprite,
                                True)
    app.dumplingsItem = Item("fennel dumplings", (0, 0), app.dumplingSprite,
                                True)
    app.porridgeItem = Item("porridge", (0, 0), app.porridgeSprite,
                                True)
    app.peachCobblerItem = Item("peach cobbler", (0, 0), app.peachCobblerSprite,
                                True)
    app.scallionNoodlesItem = Item("scallion noodles", (0, 0), app.scallionNoodlesSprite,
                                True)
    
    app.recipeNamesList = {"tomato and eggs" : app.tomatoEggItem, 
                            "apple cake" : app.appleCakeItem,
                            "fennel dumplings" : app.dumplingsItem,
                            "porridge": app.porridgeItem,
                            "peach cobbler" : app.peachCobblerItem,
                            "scallion noodles" : app.scallionNoodlesItem}

    app.recipeSprite = app.loadImage("art/recipe.png")
    app.recipeList = initializeRecipeList(app)

    app.recipeIconSprite = app.loadImage("art/recipeSprite.png")
    app.recipeIconSprite = app.scaleImage(app.recipeIconSprite, 3)
    app.recipeIcon = Icon("Recipe", (200, 75), app.recipeIconSprite)


    #HOME VARS
    room1 = app.loadImage("art/room1.jpg")
    room1 = app.scaleImage(room1, 4)
    room2 = app.loadImage("art/room2.jpg")
    room2 = app.scaleImage(room2, 4)
    app.homeBackground = [room1, room2]
    app.homeCounter = 0
    app.gameOver = False
    bed1 = app.scaleImage(app.loadImage("art/sleep1.jpg"), 4)
    bed2 = app.scaleImage(app.loadImage("art/sleep1.jpg"), 4)
    app.bedSprite = [bed1, bed2]
    app.bedSpriteCounter = 0
    app.fridgeOrder = ["eggs", "meat", "tomatoes", "water", "scallions", "fennel"]
    app.fridgeItems = [app.eggItem, app.meatItem, app.tomatoItem, app.waterItem,
                        app.scallionItem, app.fennelItem]
    app.cabinetOrder = ["flour", "rice", "sugar", "soy sauce", "noodles"]
    app.cabinetItems = [app.flourItem, app.riceItem, app.sugarItem, app.soySauceItem,
                        app.noodlesItem]
    spritestrip = app.loadImage("art/fridge.png")
    app.fridgeSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 96 * i, 96, 96 * (1 + i)))
        sprite = app.scaleImage(sprite, 3)
        app.fridgeSprite.append(sprite) #append each sprite to array

    app.homeSprite = app.loadImage("art/home.png")
    app.homeSprite = app.scaleImage(app.homeSprite, 3)
    app.homeIcon = Icon("Home", (700, 700), app.homeSprite)

    app.homeX = 0
    app.homeCameraOffset = 120
    app.displayFridge = False
    app.displayCabinet = False
    app.displayStove = False
    app.fridgeLoc = (350, 400)
    app.cabinetLoc = (200, 250)
    app.stoveLoc = (0, 400)
    app.bedLoc = (1100, 450)
    app.leftEndLoc = (-100, 450)


    #Vars related to tree or nature stuff
    app.treeSpriteCounter = 0
    spritestrip = app.loadImage("art/tree.png")
    app.treeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.treeSprite.append(sprite) #append each sprite to array

    spritestrip = app.loadImage("art/appletree.png")
    app.appleTreeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.appleTreeSprite.append(sprite) #append each sprite to array
    spritestrip = app.loadImage("art/peachTree.png")
    app.peachTreeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.peachTreeSprite.append(sprite) #append each sprite to array

    app.treeLocSet = set()
    app.frontTreeLocSet = set()
    app.behindTreeLocSet = set() 
    app.grassSprite = app.loadImage("art/grass.png")
    app.neutralGrassSprite = app.loadImage("art/neutralgrass.png")
    app.anxGrassSprite = app.loadImage("art/anxgrass.png")
    app.sadGrassSprite = app.loadImage("art/sadgrass.png")
    app.skyBackground = app.loadImage("art/sky.png")
    app.neutralFilter = app.loadImage("art/neutralFilter.png")
    app.neutralFilter = app.scaleImage(app.neutralFilter, 4)
    app.sadFilter = app.loadImage("art/sadFilter.png")
    app.sadFilter = app.scaleImage(app.sadFilter, 4)
    app.happyFilter = app.loadImage("art/happyFilter.png")
    app.happyFilter = app.scaleImage(app.happyFilter, 4)
    app.anxFilter = app.loadImage("art/anxFilter.png")
    app.anxFilter = app.scaleImage(app.anxFilter, 4)
    url = "art/flowers1.png"
    url2 = "art/flowers2.png"
    app.flowerSprite = []
    app.happyFlowerSprite = [app.loadImage(url), app.loadImage(url2)]
    app.flowerSpriteCounter = 0
    app.sadFlowerSprite = [app.loadImage("art/sadflowers.png"), 
                            app.loadImage("art/sadflowers2.png")]
    app.neutralFlowerSprite = [app.loadImage("art/neutralflowers.png"), 
                                app.loadImage("art/neutralflowers1.png")]
    app.anxFlowerSprite = [app.loadImage("art/anxflowers.png"), 
                            app.loadImage("art/anxflowers2.png")]


    #Color Variations
    app.happyColorDict = {'grass': ['#649e44', '#478f45', '#449642', '#298747'], 
                        'filter': app.happyFilter, "heightFac": 7, 
                        "grassSprite": app.grassSprite, 'density': 2}
    app.sadColorDict = {'grass': ['#4e6b5f', '#4e6b50', '#3e5e46', '#3f705e'], 
                        'filter': app.sadFilter, "heightFac": 1, 
                        "grassSprite": app.sadGrassSprite,  'density': 5}
    app.neutralColorDict = {'grass': ['#bb9429', '#cf9c30', '#d4934d', 
                            '#d4ad48'], 'filter': app.neutralFilter, 
                            "heightFac": 5, 
                            "grassSprite": app.neutralGrassSprite, 'density': 1}
    app.anxColorDict = {'grass': ['#cb5f4c', '#b54835', '#b96c46', '#c26936'], 
                        'filter': app.anxFilter, "heightFac": 20,
                        "grassSprite": app.anxGrassSprite, 'density': 10}
    
    #SOUND VARS
    pygame.mixer.init()
    app.playMusic = True
    app.sound = ""
    if (app.vibe == "happy"):
        app.vibe = app.happyColorDict
        app.sound = Sound("music/summer.mp3")
        app.timerDelay = 350
        app.flowerSprite = app.happyFlowerSprite

    elif (app.vibe == "sad"):
        app.vibe = app.sadColorDict
        app.sound = Sound("music/acoustic dream.mp3")
        app.timerDelay = 1200
        app.flowerSprite = app.sadFlowerSprite


    elif (app.vibe == "neutral"):
        app.vibe = app.neutralColorDict
        app.sound = Sound("music/the golden hour.mp3")
        app.timerDelay = 700
        app.flowerSprite = app.neutralFlowerSprite

    else:
        app.vibe = app.anxColorDict
        app.sound = Sound("music/acoustic dream.mp3")
        app.timerDelay = 150
        app.flowerSprite = app.anxFlowerSprite


    if (app.mode == "homeMode"):
        app.sound = Sound("music/tides of summer.mp3")

    app.pickingSound = pygame.mixer.Sound("music/pickupCoin.WAV")  
    app.selectSound = pygame.mixer.Sound("music/blipSelect.WAV")  
    app.openSound = pygame.mixer.Sound("music/openSound.WAV")

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
    
    gameMode_fillBoard(app, app.vibe['grass'], app.grassColorBoard)
    changeTreeList(app)
    if (app.playMusic):
        app.sound.start(loops = -1)

#Credits see top

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
    r, c = r + 2, c + 1
    return r, c


#returns true if player x, y is within row, col bounds
def homeMode_constraintsMet(app, x, dir):
    x, y = app.playerPos
    if (x >= app.bedLoc[0] and dir == "left"):
        return True
    elif (x <= app.leftEndLoc[0] and dir == "right"):
        return True
    return (x > app.leftEndLoc[0] and x <= app.bedLoc[0])

def gameMode_constraintsMet(app, x, y, dir):
    row, col = getPlayerRowCol(app, x, y)
    if (row == 1 and dir == "up" or (col == 1 and dir == "up")):
        return False
    else:
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
    return (abs(event.x - other[0]) <= 100 and abs(event.y - other[1]) <= 100)


def startScreen_mousePressed(app, event):
    if (withinRange(app, event, app.startLoc)):
        app.mode = "gameMode"
        app.prevMode = "gameMode"
        pygame.mixer.find_channel().play(app.openSound)
    elif (withinRange(app, event, app.helpLoc)):
        app.isHelp = True
        pygame.mixer.find_channel().play(app.openSound)
    if (app.closeIcon.mouseClickedNear(event)):
        app.isHelp = False
        pygame.mixer.find_channel().play(app.selectSound)

def homeMode_keyReleased(app, event):
    if (event.key == 'Right'):
        app.lastPressedKey = "Right"
    elif (event.key == 'Left'):
        app.lastPressedKey = "Left"   



def homeMode_mousePressed(app, event):
    if (app.displayJournal):
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayJournal = False
            pygame.mixer.find_channel().play(app.selectSound)
            #once done with reading journal, change into writing mode
            app.journal = open("journal.txt", "a+")
    elif (app.journalIcon.mouseClickedNear(event)):
        pygame.mixer.find_channel().play(app.openSound)
        app.displayJournal = True 
        if (app.displayJournal):
            app.journal.close()
            #change it into reading mode to display text
            app.journal = open("journal.txt", "r")
            fillJournalDict(app)

    if (withinRange(app, event, app.stoveLoc) and not (app.displayFridge or app.displayCabinet)):
        app.displayStove = True
        pygame.mixer.find_channel().play(app.openSound)
    if (withinRange(app, event, app.fridgeLoc) and not (app.displayCabinet or app.displayStove)):
        app.displayFridge = True
        pygame.mixer.find_channel().play(app.openSound)
    if (withinRange(app, event, app.cabinetLoc) and not (app.displayFridge or app.displayStove)):
        app.displayCabinet = True
        pygame.mixer.find_channel().play(app.openSound)

    if (app.recipeIcon.mouseClickedNear(event)):
        app.displayRecipe = True
        pygame.mixer.find_channel().play(app.openSound)

    elif (app.displayRecipe):
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayRecipe = False
            pygame.mixer.find_channel().play(app.selectSound)

    if (app.inventoryIcon.mouseClickedNear(event) and 
        not (app.displayCabinet or app.displayFridge or app.displayStove)):
        if (app.displayInventory): #is open, so play closing sound
            pygame.mixer.find_channel().play(app.selectSound)

        else:
            pygame.mixer.find_channel().play(app.openSound)

        app.displayInventory = not app.displayInventory

    if (app.displayInventory):
        for item in app.inventoryList:
            if item.mouseClickedNear(event):
                if (item.eat()):
                    item.count -= 1
                    app.homeText = f"you ate {item.name}!"
                    app.homeTextTimer = 3
                else:
                    app.homeText = f"this item cannot be eaten"
                    app.homeTextTimer = 3


    if app.displayFridge:
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayFridge = False
            pygame.mixer.find_channel().play(app.selectSound)
        for item in app.fridgeItems:
            if item.mouseClickedNear(event):
                if (item not in app.inventoryList):
                    app.inventoryList.append(item)
                app.homeText = f"{item.name} + 1"
                app.homeTextTimer = 3
                item.count += 1
                pygame.mixer.find_channel().play(app.openSound)
                app.lastClickedLoc = (item.loc[0], item.loc[1] - 50)

    if app.displayCabinet:
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayCabinet = False
            pygame.mixer.find_channel().play(app.selectSound)
        for item in app.cabinetItems:
            if item.mouseClickedNear(event):
                if (item not in app.inventoryList):
                    app.inventoryList.append(item)
                app.homeText = f"{item.name} + 1"
                app.homeTextTimer = 3
                item.count += 1
                pygame.mixer.find_channel().play(app.openSound)
                app.lastClickedLoc = (item.loc[0], item.loc[1] - 50)

    if app.displayStove:
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayStove = False
            pygame.mixer.find_channel().play(app.selectSound)
        canCook = True
        #app.recipeList is recipe items... i think
        for recipe in app.recipeList:
            if withinRange(app, event, recipe.loc):
                #ex tomato and eggs has {tomato : 3, eggs : 2, etc.}
                recipeDict = recipe.ingredients
                curIngredientCount = 0
                for ingredient in recipeDict: 
                    for item in app.inventoryList:
                        if (ingredient == item.name and item.count >= recipeDict[ingredient]):
                            curIngredientCount += 1
                #check if cancook, ex. if player has 3 tomatoes and 2 eggs
                if (curIngredientCount != len(recipeDict)):
                    canCook = False
                    app.homeText = "insufficient ingredients!"
                    pygame.mixer.find_channel().play(app.selectSound)
                    app.homeTextTimer = 3
                if (canCook):
                    for ingredient in recipeDict: 
                        for item in app.inventoryList:
                            if (ingredient == item.name):
                                item.count -= recipeDict[ingredient]
                        #remove used ingredients
                    app.homeText = f"cooked {recipe.name}!"
                    pygame.mixer.find_channel().play(app.openSound)
                    app.homeTextTimer = 3
                    recipeItem = app.recipeNamesList[f"{recipe.name}"]
                    if (recipeItem not in app.inventoryList):
                        app.inventoryList.append(recipeItem)
                    recipeItem.count += 1
                    

def gameMode_mousePressed(app, event):
    if (app.displayJournal):
        if (app.rightArrowIcon.mouseClickedNear(event)):
            if (app.currentPage < len(app.journalDict) - 1):
                app.currentPage += 1
                pygame.mixer.find_channel().play(app.openSound)
        elif (app.leftArrowIcon.mouseClickedNear(event)):
            if (app.currentPage == 0):
                pass #don't go to next page if current page is max page
            else:
                app.currentPage -= 1
                pygame.mixer.find_channel().play(app.openSound)

        if (app.closeIcon.mouseClickedNear(event)):
            app.displayJournal = False
            #once done with reading journal, change into writing mode
            app.journal = open("journal.txt", "a+")
            pygame.mixer.find_channel().play(app.selectSound)
    elif (app.journalIcon.mouseClickedNear(event)):
        app.displayJournal = True 
        if (app. displayJournal):
            app.journal.close()
            #change it into reading mode to display text
            app.journal = open("journal.txt", "r")
            fillJournalDict(app)
        pygame.mixer.find_channel().play(app.openSound)

    elif (app.recipeIcon.mouseClickedNear(event)):
        app.displayRecipe = True
        pygame.mixer.find_channel().play(app.openSound)
    elif (app.displayRecipe):
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayRecipe = False
        pygame.mixer.find_channel().play(app.selectSound)
    elif (app.inventoryIcon.mouseClickedNear(event)):
        if (app.displayInventory): #is open, so play closing sound
            pygame.mixer.find_channel().play(app.selectSound)
        else:
            pygame.mixer.find_channel().play(app.openSound)
        app.displayInventory = not app.displayInventory
    elif (app.helpIcon.mouseClickedNear(event)):
        app.isHelp = True
        pygame.mixer.find_channel().play(app.selectSound)
    elif (app.isHelp):
        if (app.closeIcon.mouseClickedNear(event)):
            app.isHelp = False
    elif (app.homeIcon.mouseClickedNear(event)):
        pygame.mixer.find_channel().play(app.openSound)
        app.text = ""
        app.playerPos = (400, 450)
        # update vars for home
        app.playerSprite = app.leftHomeIdleSprite
        app.goHome = True
        app.timerDelay = 500
        app.sound = Sound("music/tides of summer.mp3")
        if (app.playMusic):
            app.sound.start(loops = -1)
        app.mode = "homeMode"
    else:
        cx, cy = app.playerPos
        playerRow, playerCol = getPlayerRowCol(app, cx, cy)
        for tree in app.treeList:
            if (tree.mouseClickedNear(app, event) and type(tree) == FruitTree):
                if not (tree.fruitPicked):
                    tree.fruitPicked = True
                    pygame.mixer.find_channel().play(app.pickingSound)
                    tree.changeTree(app)
                    if (tree.fruit == "apples"):
                        app.appleItem.count += 3
                        if (app.appleItem not in app.inventoryList):
                            #inventoryList stores list of ITEMS not their names
                            app.inventoryList.append(app.appleItem)
                    else:
                        app.peachItem.count += 3
                        if (app.peachItem not in app.inventoryList):
                            #inventoryList stores list of ITEMS not their names
                            app.inventoryList.append(app.peachItem)
                    app.homeTextTimer = 3
                    app.lastClickedLoc = (cx, cy - 120)
                    app.homeText = f"{tree.fruit} + 3"
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
            app.bedLoc = (app.bedLoc[0] + app.homeCameraOffset, app.bedLoc[1])
            app.leftEndLoc = (app.leftEndLoc[0] + app.homeCameraOffset, app.leftEndLoc[1])

    elif (dir == "right"):
        if (x >= app.width - app.boundingBoxLimit):
            app.homeX += app.homeCameraOffset
            app.stoveLoc = (app.stoveLoc[0] - app.homeCameraOffset, app.stoveLoc[1])
            app.fridgeLoc = (app.fridgeLoc[0] - app.homeCameraOffset, app.fridgeLoc[1])
            app.cabinetLoc = (app.cabinetLoc[0] - app.homeCameraOffset, app.cabinetLoc[1])
            app.bedLoc = (app.bedLoc[0] - app.homeCameraOffset, app.bedLoc[1])
            app.leftEndLoc = (app.leftEndLoc[0] - app.homeCameraOffset, app.leftEndLoc[1])

def homeMode_keyPressed(app, event):
    cx, cy = app.playerPos
    if (app.goBedConfirm):
        if (event.key == "g"):
            app.goBed = True
        else:
            app.goBedConfirm = False
    if (app.goBed):
        if (event.key == "h"):
            app.cheatMood = "happy"
            app.isCheat = True
        elif (event.key == "s"):
            app.cheatMood = "sad"
            app.isCheat = True
        elif (event.key == "a"):
            app.cheatMood = "anx"
            app.isCheat = True
        elif (event.key == "l"):
            app.cheatMood = "neutral"
            app.isCheat = True

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
        elif (event.key == "n"):
            app.gameOver = True

    if (event.key == 'Right'):
        if (homeMode_constraintsMet(app, cx + app.speed, "right")):
            app.playerPos = (cx + app.speed, cy)
            app.playerHomeSprite = app.rightHomeWalkSprite
            homeMode_moveCamera(app, "right")
    if (event.key == 'Left'):
        if (homeMode_constraintsMet(app, cx - app.speed, "left")):
            app.playerPos = (cx - app.speed, cy)
            app.playerHomeSprite = app.leftHomeWalkSprite
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
        if (event.key == 'Enter'):
            app.journal.write(app.text + "\n")
            app.text = ""
            app.textLenChecker = 0

    #Player movement
    if (event.key == 'Up'):
        if gameMode_constraintsMet(app, cx, cy - app.speed, "up"):
            app.playerPos = (cx, cy - app.speed)
            app.playerSprite = app.backWalkSprite
            gameMode_moveCamera(app, "up")
    elif (event.key == 'Down'):
        if gameMode_constraintsMet(app, cx, cy + app.speed, "down"):
            app.playerPos = (cx, cy + app.speed)
            app.playerSprite = app.frontWalkSprite
            gameMode_moveCamera(app, "down")
    elif (event.key == 'Right'):
        if gameMode_constraintsMet(app, cx + app.speed, cy, "right"):
            app.playerPos = (cx + app.speed, cy)
            app.playerSprite = app.rightWalkSprite
            gameMode_moveCamera(app, "right")
    elif (event.key == 'Left'):
        if gameMode_constraintsMet(app, cx - app.speed, cy, "left"):
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

def getRowCol(app, x, y):
    row = (y - app.margin)//app.cellSize
    col = (x - app.margin)/app.cellSize
    return row, col

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
    newL.append(Recipe("fennel dumplings", {"meat" : 2, "fennel" : 3, "flour" : 2},
                        app.dumplingSprite))
    newL.append(Recipe("porridge", {"rice" : 3, "water" : 3, "eggs" : 2, "scallions" : 2},
                        app.porridgeSprite))
    newL.append(Recipe("apple cake", {"flour" : 2, "apples" : 2, "eggs" : 2, "water" : 2},
                        app.appleCakeSprite))
    newL.append(Recipe("peach cobbler", {"peaches" : 3, "flour" : 2, "eggs" : 1, "water" : 1},
                        app.peachCobblerSprite))
    newL.append(Recipe("scallion noodles", {"scallions" : 2, "noodles" : 2, "soy sauce" : 1, "water" : 1},
                        app.scallionNoodlesSprite))
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

def fillJournalDict(app):
    app.journal.seek(0)
    lines = app.journal.readlines()
    app.journalDict = dict()
    for i in range(0, len(lines)):
        app.journalDict[i//40] = app.journalDict.get(i//40, []) + [lines[i]]

def changeTreeList(app):
    playerX, playerY = app.playerPos
    for i in range(len(app.treeList)):
        tree = app.treeList[i]
        cx, cy = tree.getCenter(app)
        if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
            if (cy < playerY + 42): #tree is behind player
                tree.isFront = False
            if (cy >= playerY + 42): #tree is in front of player
                tree.isFront = True

def homeMode_timerFired(app):
    x, y = app.playerPos
    if (x >= app.bedLoc[0]):
        app.goBedConfirm = True
    if app.homeCounter == 1:
        app.homeCounter = 0
    else:
        app.homeCounter = 1
    app.homeTextTimer -= 1
    if (app.homeTextTimer == 0): #messages stay for 3 * app.timerDelay secs
        app.homeTextTimer = 0
    if app.bedSpriteCounter == 1:
        app.bedSpriteCounter = 0
    else:
        app.bedSpriteCounter = 1
    app.homeSpriteCounter = (1 + app.homeSpriteCounter) % len(app.playerHomeSprite)
    app.lastPressedCounter += 1
    if (app.lastPressedCounter >= 1):
        if (app.lastPressedKey == 'Right'):
            app.playerHomeSprite = app.rightHomeIdleSprite
        elif (app.lastPressedKey == 'Left'):
            app.playerHomeSprite = app.leftHomeIdleSprite   
        app.lastPressedCounter = 0
    app.lastClickedLoc = (app.lastClickedLoc[0], app.lastClickedLoc[1] - 10)

def gameMode_timerFired(app):
    moveClouds(app)
    app.playerSpriteCounter = (1 + app.playerSpriteCounter) % len(app.playerSprite)
    app.treeSpriteCounter = (1 + app.treeSpriteCounter) % len(app.treeSprite)
    app.lastPressedCounter += 1
    if (app.lastPressedCounter >= 1): #waits a bit before changing animation
        if (app.lastPressedKey == 'Up'):
            app.playerSprite = app.backIdleSprite
        elif (app.lastPressedKey == 'Down'):
            app.playerSprite = app.frontIdleSprite
        elif (app.lastPressedKey == 'Right'):
            app.playerSprite = app.rightIdleSprite
        elif (app.lastPressedKey == 'Left'):
            app.playerSprite = app.leftIdleSprite   
        app.lastPressedCounter = 0
    if app.flowerSpriteCounter == 1:
        app.flowerSpriteCounter = 0
    else:
        app.flowerSpriteCounter = 1
    app.lastClickedLoc = (app.lastClickedLoc[0], app.lastClickedLoc[1] - 10)
    app.homeTextTimer -= 1
    if (app.homeTextTimer == 0): #messages stay for 3 * app.timerDelay secs
        app.homeTextTimer = 0

#---------------------------------------
# JOURNAL FUNCTIONS
# --------------------------------------
def detectWords(app):
    app.journal.seek(0)
    lines = app.journal.readlines()
    dayCount = 0
    for wordIndex in range(len(lines) - 1, -1, -1):
        word = lines[wordIndex]
        if ("/" in word):
            curDate = lines.index(word)
            dayCount += 1
            if (dayCount >= 3):
                lines = lines[curDate:] 
                #gets journal entries from past three days
                break
    lines = " ".join(lines)
    app.feelingsDict = te.get_emotion(lines)
    # print(app.feelingsDict)
    changeColors(app)

def changeColors(app):
    largestMood = "Happy"
    largestMoodCount = 0.0
    for feeling in app.feelingsDict:
        # print(feeling, app.feelingsDict[feeling])
        if app.feelingsDict[feeling] > largestMoodCount:
            largestMood = feeling
            largestMoodCount = app.feelingsDict[feeling]
    if (largestMood == "Happy"):
        largestMood = "happy"
    elif (largestMood == "Fear" or largestMood == "Surprise"):
        largestMood = "neutral"
    elif (largestMood == "Anger"):
        largestMood = "anx"
    else:
        largestMood = "sad"
    if (app.isCheat):
        largestMood = app.cheatMood
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
                chance = random.randint(1, 4)
                if (chance == 1):
                    app.treeList.append(Tree(app, row, col))
                elif (chance == 2):
                    app.treeList.append(FruitTree(app, row, col, "apples", app.appleTreeSprite))
                else:
                    app.treeList.append(FruitTree(app, row, col, "peaches", app.peachTreeSprite))



def gameMode_moveCamera(app, dir):
    #if player is a certain amount of distance away from the screen
    x, y = app.playerPos
    if (dir == "left"):
        if (x <= app.boundingBoxLimit):
            app.prevX -= app.cameraOffset
            app.playerPos = (x + app.cameraOffset, y)
    elif (dir == "right"):
        if (x >= app.width - app.boundingBoxLimit):
            app.prevX += app.cameraOffset
            app.playerPos = (x - app.cameraOffset, y)
    elif (dir == "up"):
        if (y <= app.boundingBoxLimit):
            app.prevY -= app.cameraOffset
            app.playerPos = (x, y + app.cameraOffset)

    elif (dir == "down"): 
        if (y >= app.height - app.boundingBoxLimit):
            app.prevY += app.cameraOffset
            app.playerPos = (x, y - app.cameraOffset)


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
            canvas.create_image(cx, cy, image=grass)
        elif (color == colorList[3]):
            grass = app.flowerSprite[app.flowerSpriteCounter]
            grass = getCachedPhotoImage(app, grass)
            canvas.create_image(cx, cy - yOffsetTopL, image=grass)
        

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

def homeMode_drawEndScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "black")
    canvas.create_text(app.width//2, app.height//2, text = "thank you for playing!",
                        font = f"{app.font} 24 bold", fill = "white")
def gameMode_drawRecipeBook(app, canvas):
    filter = app.sadFilter
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    i = 0
    canvas.create_text(200, 175 , text = "recipes", font= f"{app.font} 24 bold",
                        anchor = "n")
    startX = 180
    startY = 230
    xOffset = 350
    for recipe in app.recipeList:
        if (i >= 12):
            #draw on other half of screen
            canvas.create_text(startX + xOffset, startY + (i - 12) * 25, text = recipe.name, 
                font = f"{app.font} 12 bold")
            recipe.loc = (startX + xOffset, startY + (i - 12) * 25)
            img = getCachedPhotoImage(app, recipe.sprite)
            canvas.create_image(startX + xOffset + 140, startY + (i - 12) * 25, image=img)
            for item in recipe.ingredients: #draw ingredients
                i += 1
                canvas.create_text(startX + xOffset, startY + (i - 12) * 25, text = f"{item} : {recipe.ingredients[item]}",
                font = f"{app.font} 12")
            i += 1
        else: 
            #draw on first half of screen
            canvas.create_text(startX, startY + i * 30, text = recipe.name, 
                font = f"{app.font} 12 bold")
            img = getCachedPhotoImage(app, recipe.sprite)
            canvas.create_image(startX + 140, startY + i * 30, image=img)
            recipe.loc = (startX, startY + i * 30)
            for item in recipe.ingredients:
                i += 1
                canvas.create_text(startX, startY + i * 30, text = f"{item} : {recipe.ingredients[item]}",
                font = f"{app.font} 12")
            i += 1
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(75, 200, image=journalClose)


def gameMode_drawInventory(app, canvas):
    rows, cols = len(app.inventoryGrid), len(app.inventoryGrid[0])
    filter = app.sadFilter
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    iconBg = app.scaleImage(app.sadFilter, 1/8)
    iconBg = getCachedPhotoImage(app, iconBg)
    inventoryIndex = 0
    for row in range(rows):
        for col in range(cols):
            x0 = col * 100 + app.margin
            x1 = (col + 1) * 100 + app.margin
            y0 = row * 100 + app.margin
            y1 = (row + 1) * 100 + app.margin
            if (2 <= row <= 5 and 2 <= col <= 5):
                canvas.create_image((x0 + x1)/2, (y0 + y1)/2, image = iconBg)
                if (inventoryIndex < len(app.inventoryList)):
                    item = app.inventoryList[inventoryIndex]
                    sprite = item.sprite
                    sprite = getCachedPhotoImage(app, sprite)
                    canvas.create_image((x0 + x1)/2, (y0 + y1)/2, image= sprite)
                    canvas.create_text((x0 + x1)/2, y0, text = f"{item.name} : {item.count}",
                                        font = f"{app.font} 10", anchor = "n")
                    inventoryIndex += 1
    canvas.create_text(250, 150, text = "inventory",
                    font = f"{app.font} 14 bold", anchor = "n", fill = "black")


def gameMode_drawPlayer(app, canvas):
    x, y = app.playerPos
    player = getCachedPhotoImage(app, app.playerSprite[app.playerSpriteCounter])
    canvas.create_image(x, y, image = player)


def homeMode_drawPlayer(app, canvas):
    x, y = app.playerPos
    player = getCachedPhotoImage(app, app.playerHomeSprite[app.homeSpriteCounter])
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
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    canvas.create_text(200, 220, text = "journal", 
                        font = f"{app.font} 24 bold", anchor = "s")
    i = 0
    app.journal.seek(0)
    lines = app.journal.readlines()
    #only display 40 lines at a time
    for line in app.journalDict[app.currentPage]:
        if (i >= 20): 
            #put on next half of page
            canvas.create_text (600, 250 + (i - 20) * 20, text = line, 
            font = f"{app.font} 12")
        else:
            canvas.create_text (200, 230 + i * 20, text = line, 
            font = f"{app.font} 12")
        i += 1

    canvas.create_text(100, 700, text = f"page {app.currentPage + 1}",
                        font = f"{app.font} 24 bold")
    leftArrow = getCachedPhotoImage(app, app.leftArrowIcon.sprite)
    canvas.create_image(app.leftArrowIcon.loc[0], app.leftArrowIcon.loc[1], image=leftArrow)
    rightArrow = getCachedPhotoImage(app, app.rightArrowIcon.sprite)
    canvas.create_image(app.rightArrowIcon.loc[0], app.rightArrowIcon.loc[1], image=rightArrow)

    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(75, 200, image=journalClose)

def gameMode_drawTextAndUI(app, canvas):
    filter = app.vibe["filter"]
    filter = getCachedPhotoImage(app, filter)
    canvas.create_image(400, 400, image= filter)
    journalOpen = getCachedPhotoImage(app, app.journalIcon.sprite)
    canvas.create_image(app.journalIcon.loc[0], app.journalIcon.loc[1], image=journalOpen)
    homeIc = getCachedPhotoImage(app, app.homeIcon.sprite)
    canvas.create_image(app.homeIcon.loc[0], app.homeIcon.loc[1], image= homeIc)
    inventoryIc = getCachedPhotoImage(app, app.inventoryIcon.sprite)
    canvas.create_image(app.inventoryIcon.loc[0], app.inventoryIcon.loc[1], image= inventoryIc)
    recipeIc = getCachedPhotoImage(app, app.recipeIcon.sprite)
    canvas.create_image(app.recipeIcon.loc[0], app.recipeIcon.loc[1], image= recipeIc)
    helpIc = getCachedPhotoImage(app, app.helpIcon.sprite)
    canvas.create_image(app.helpIcon.loc[0], app.helpIcon.loc[1], image= helpIc)
    canvas.create_text(app.width//2, 700, text = f"{app.text}", fill = "white",
                        font = "Fixedsys 24 bold", anchor = "s")

    if (app.homeTextTimer > 0):
        homeMode_drawText(app, canvas, app.lastClickedLoc)


def gameMode_drawTreesInBack(app, canvas):
    for tree in app.treeList:
        if not (tree.isFront):
            cx, cy = tree.getCenter(app)
            if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
                tree = getCachedPhotoImage(app, tree.sprite[app.treeSpriteCounter])
                canvas.create_image(cx, cy - 120, image=tree)

def gameMode_drawTreesInFront(app, canvas):
    for tree in app.treeList:
        if (tree.isFront):
            cx, cy = tree.getCenter(app)
            if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
                tree = getCachedPhotoImage(app, tree.sprite[app.treeSpriteCounter])
                canvas.create_image(cx, cy - 120, image=tree)


def gameMode_drawBackground(app, canvas):
    sky = getCachedPhotoImage(app, app.skyBackground)
    canvas.create_image(app.width//2, app.width//2, image=sky)


def homeMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    home = getCachedPhotoImage(app, app.homeBackground[app.homeCounter])
    canvas.create_image(400 - app.homeX, 400, image = home)


def homeMode_drawText(app, canvas, loc):
    canvas.create_text(int(loc[0]), int(loc[1]), text = f"{app.homeText}", 
                        font = f"{app.font} 12 bold", fill = "white")

def homeMode_drawBed(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    bed = getCachedPhotoImage(app, app.bedSprite[app.bedSpriteCounter])
    canvas.create_image(400, 400, image = bed)

    canvas.create_text(app.width/2, app.height/2 + 200, 
                        text = "you went to bed for the day", 
                        fill = "white", font = f"{app.font} 18")
    canvas.create_text(app.width/2, app.height/2 + 250, 
                        text = "go out again the next morning? (y/n)",
                        fill = "white", font = f"{app.font} 18")

def homeMode_drawStove(app, canvas):
    gameMode_drawRecipeBook(app, canvas)
    canvas.create_text(600, 200, text = "time to cook!", font = f"{app.font} 18 bold")

def homeMode_drawCabinet(app, canvas):
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)
    rows, cols = len(app.inventoryGrid), len(app.inventoryGrid[0])
    iconBg = app.scaleImage(app.sadFilter, 1/8)
    iconBg = getCachedPhotoImage(app, iconBg)
    canvas.create_text(250, 175, text = "cabinet", 
                    font = f"{app.font} 18 bold", fill = "white")
    cabinetIndex = 0
    for row in range(rows):
        for col in range(cols):
            x0 = col * 100 + app.margin
            x1 = (col + 1) * 100 + app.margin
            y0 = row * 100 + app.margin
            y1 = (row + 1) * 100 + app.margin
            if (2 <= row <= 4 and 2 <= col <= 5):
                canvas.create_image((x0 + x1)/2, (y0 + y1)/2, image = iconBg)
                if (cabinetIndex < len(app.cabinetItems)):
                    item = app.cabinetItems[cabinetIndex]
                    sprite = item.sprite
                    sprite = getCachedPhotoImage(app, sprite)
                    cx, cy = (x0 + x1)/2, (y0 + y1)/2
                    canvas.create_image(cx, cy, image= sprite)
                    item.loc = (cx, cy)
                    canvas.create_text(cx, y0, text = f"{item.name}",
                                        font = f"{app.font} 10", anchor = "n")
                    cabinetIndex += 1

def homeMode_drawFridge(app, canvas):
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)
    rows, cols = len(app.inventoryGrid), len(app.inventoryGrid[0])
    iconBg = app.scaleImage(app.sadFilter, 1/8)
    iconBg = getCachedPhotoImage(app, iconBg)
    canvas.create_text(250, 175, text = "fridge", 
                    font = f"{app.font} 18 bold", fill = "white")
    fridgeIndex = 0
    for row in range(rows):
        for col in range(cols):
            x0 = col * 100 + app.margin
            x1 = (col + 1) * 100 + app.margin
            y0 = row * 100 + app.margin
            y1 = (row + 1) * 100 + app.margin
            if (2 <= row <= 4 and 2 <= col <= 5):
                canvas.create_image((x0 + x1)/2, (y0 + y1)/2, image = iconBg)
                if (fridgeIndex < len(app.fridgeItems)):
                    item = app.fridgeItems[fridgeIndex]
                    sprite = item.sprite
                    sprite = getCachedPhotoImage(app, sprite)
                    cx, cy = (x0 + x1)/2, (y0 + y1)/2
                    canvas.create_image(cx, cy, image= sprite)
                    item.loc = (cx, cy)
                    canvas.create_text(cx, y0, text = f"{item.name}",
                                        font = f"{app.font} 10", anchor = "n")
                    fridgeIndex += 1


def homeMode_drawUI(app, canvas):
    if (app.goBedConfirm):
        canvas.create_text(app.bedLoc[0], app.bedLoc[1] - 100, text = "go to bed? (g to confirm)",
                            font = f"{app.font} 14 bold", fill = "white")
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
        
    if (app.displayJournal):
        gameMode_drawJournal(app, canvas)
    
    if (app.homeTextTimer > 0):
        homeMode_drawText(app, canvas, app.lastClickedLoc)

    journalOpen = getCachedPhotoImage(app, app.journalIcon.sprite)
    canvas.create_image(app.journalIcon.loc[0], app.journalIcon.loc[1], image=journalOpen)
    inventoryIc = getCachedPhotoImage(app, app.inventoryIcon.sprite)
    canvas.create_image(app.inventoryIcon.loc[0], app.inventoryIcon.loc[1], image= inventoryIc)
    recipeIc = getCachedPhotoImage(app, app.recipeIcon.sprite)
    canvas.create_image(app.recipeIcon.loc[0], app.recipeIcon.loc[1], image= recipeIc)


def drawHelpMode(app, canvas):
    filter = getCachedPhotoImage(app, app.sadFilter)
    canvas.create_image(400, 400, image= filter)
    journalClose = getCachedPhotoImage(app, app.journalCloseSprite)
    canvas.create_image(100, 200, image=journalClose)
    canvas.create_text(400, 50, text = "help mode", font = "Fixedsys 18 bold",
                        fill = "dark blue")
    tutorialText = ["use the arrow keys to move",
                     "click on fruit and plants to pick them",
                     "check what items you have in the inventory",
    "type to write in journal", "(who knows, something might change the next day!)",
                "be sure to check which recipes you can cook before you go home!",
                 "go to bed at home to move onto the next day"]
    for i in range(len(tutorialText)):
        canvas.create_text(400, 100 + (30 * i), text = f"{tutorialText[i]}",
                            font = "Fixedsys 14", fill = "black")



def startScreen_redrawAll(app, canvas):
    gameMode_drawBackground(app, canvas)
    gameMode_drawClouds(app, canvas)
    filter = getCachedPhotoImage(app, app.happyFilter)
    canvas.create_image(400, 400, image= filter)

    canvas.create_text(400, 450, text = "perennial summer.", fill = "#0d2352",
                        font = "Fixedsys 48 bold")
    canvas.create_text(app.startLoc[0], app.startLoc[1], text = "start", fill = "#386C9D",
                        font = "Fixedsys 24 bold")
    canvas.create_text(app.helpLoc[0], app.helpLoc[1], text = "help", fill = "#386C9D",
                        font = "Fixedsys 24 bold")
    if (app.isHelp):
        drawHelpMode(app, canvas)
    

def homeMode_redrawAll(app, canvas):
    if (app.gameOver):
        homeMode_drawEndScreen(app, canvas)
    elif (app.goBed):
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
    if (app.isHelp):
            drawHelpMode(app, canvas)
    

runApp(width = 800, height = 800) 