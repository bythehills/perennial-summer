from cmu_112_graphics import *
import random
import pygame
import text2emotion as te

'''
to-do - perennial summer
11/29 - finish UI for home, journal, inventory, recipe, inventory done
11/30 - add sound and start + end screen + sleep screen, 
        fancier lighting overlays (i give up on this)
        , add flowers (done) and GRASS (to do....)
        eat recipes
        (i have tues 12 - 7 ish, 9 - whenever to work on this)
12/1 - add birds, misc bug fixes (in front/ behind trees),
        then i will be free.... so close.... yet so far
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
#list of fonts from https://stackoverflow.com/questions/39614027/list-available-
# font-families-in-tkinter/47415907
# Channels code from https://stackoverflow.com/questions/53617967/play-music-and
# -sound-effects-on-top-of-each-other-pygame
#Sound effects created with https://sfxr.me/

#Sprite-related code (spritesheet, spritecounter, cropping) from:
#also scaling image code and screen mode code
#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html

#Text to emotion module and code taken from
#https://towardsdatascience.com/text2emotion-python-package-to-detect-emotions-
# from-textual-data-b2e7b7ce1153

#All art by me, inspiration taken from Animal Crossing (for trees)
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
    app.mode = "startScreen"
    #START SCREEN VARIABLES 
    app.startLoc = (300, 550)
    app.helpLoc = (500, 550)
    app.helpSprite = app.loadImage("helpSprite.png")
    app.helpSprite = app.scaleImage(app.helpSprite, 1.5)
    app.helpIcon = Icon("Help", (100, 700), app.helpSprite)
    app.isHelp = False

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
    app.brdWidth = 0
    app.playerDir = ""
    app.cameraOffset = 100
    app.boundingBoxLimit = 200
    app.prevX = 500
    app.prevY = 500
    app.skyColor = ["#6197ed"]
    app.timerDelay = 300
    app.timeSinceLastCloud = 0
    app.treeList = []
    app.behindTreeList = []
    app.frontTreeList = []
    app.font = "Fixedsys"
    app.homeTextTimer = 3
    app.homeText = ""


    #INVENTORY VARS
    app.displayInventory = False
    app.inventoryGrid = [[0] * 7 for row in range(7)]
    #this stores order in which to draw items
    app.inventoryList = []
    app.inventory = open("inventory.txt", "r")
    url = "inventory.png"
    app.inventorySprite = app.loadImage(url)
    app.inventorySprite = app.scaleImage(app.inventorySprite, 3)
    app.inventoryIcon = Icon("Inventory", (700, 75), app.inventorySprite)

    fillInventory(app) #fill inventory across days
    app.inventory.close()
    #REMINDER: have to have inventoryDict write to inventory file

    #INITIALIZE ITEMS (This includes recipes)
    app.appleSprite = app.loadImage("apple.png")
    app.appleSprite = app.scaleImage(app.appleSprite, 1)
    app.appleItem = Item("apples", (0, 0), app.appleSprite, True)
    app.eggSprite = app.loadImage("eggs.png")
    app.eggSprite = app.scaleImage(app.eggSprite, 1)
    app.eggItem = Item("eggs", (0, 0), app.eggSprite, False)
    app.flourSprite = app.loadImage("flour.png")
    app.flourSprite = app.scaleImage(app.flourSprite, 1)
    app.flourItem = Item("flour", (0, 0), app.flourSprite, False)
    app.peachSprite = app.loadImage("peach.png")
    app.peachSprite = app.scaleImage(app.peachSprite, 1)
    app.peachItem = Item("peaches", (0, 0), app.peachSprite, True)
    app.noodleSprite = app.loadImage("noodles.png")
    app.noodleSprite = app.scaleImage(app.noodleSprite, 1)
    app.noodlesItem = Item("noodles", (0, 0), app.noodleSprite, False)
    app.riceSprite = app.loadImage("rice.png")
    app.riceSprite = app.scaleImage(app.riceSprite, 1)
    app.riceItem = Item("rice", (0, 0), app.riceSprite, False)
    app.waterSprite = app.loadImage("water.png")
    app.waterSprite = app.scaleImage(app.waterSprite, 1)
    app.waterItem = Item("water", (0, 0), app.waterSprite, True)
    app.tomatoSprite = app.loadImage("tomato.png")
    app.tomatoSprite = app.scaleImage(app.tomatoSprite, 1)
    app.tomatoItem = Item("tomatoes", (0, 0), app.tomatoSprite, True)
    app.soySauceSprite = app.loadImage("soy sauce.png")
    app.soySauceSprite = app.scaleImage(app.soySauceSprite, 1)
    app.soySauceItem = Item("soy sauce", (0, 0), app.soySauceSprite, False)
    app.sugarSprite = app.loadImage("sugar.png")
    app.sugarSprite = app.scaleImage(app.sugarSprite, 1)
    app.sugarItem = Item("sugar", (0, 0), app.sugarSprite, False)
    app.meatSprite = app.loadImage("meat.png")
    app.meatSprite = app.scaleImage(app.meatSprite, 1)
    app.meatItem = Item("meat", (0, 0), app.meatSprite, False)
    app.scallionSprite = app.loadImage("scallion.png")
    app.scallionSprite = app.scaleImage(app.scallionSprite, 1)
    app.scallionItem = Item("scallion", (0, 0), app.scallionSprite, False)
    app.fennelSprite = app.loadImage("fennel.png")
    app.fennelSprite = app.scaleImage(app.fennelSprite, 1)
    app.fennelItem = Item("fennel", (0, 0), app.fennelSprite, False)
    # app.plantList = [] #this is a list of PLANTSSSS not ITEMS

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
    url = "journalopen.png"
    app.journalOpenSprite = app.loadImage(url)
    url = "journalclose.png"
    app.journalCloseSprite = app.loadImage(url)
    app.journalOpenSprite = app.scaleImage(app.journalOpenSprite, 1)
    app.journalIcon = Icon("Journal", (75, 75), app.journalOpenSprite)
    app.closeIcon = Icon("Close", (75, 200), app.journalCloseSprite)

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

    app.scallionNoodlesSprite = app.loadImage("scallionnoodles.png")
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


    url = "recipe.png"
    app.recipeSprite = app.loadImage(url)
    app.hungerMeter = random.randint(50, 100)
    app.recipeList = initializeRecipeList(app)

    app.recipeIconSprite = app.loadImage("recipeSprite.png")
    app.recipeIconSprite = app.scaleImage(app.recipeIconSprite, 3)
    app.recipeIcon = Icon("Recipe", (200, 75), app.recipeIconSprite)


    #HOME VARS
    url = "room1.jpg"
    room1 = app.loadImage(url)
    room1 = app.scaleImage(room1, 4)
    url = "room2.jpg"
    room2 = app.loadImage(url)
    room2 = app.scaleImage(room2, 4)
    app.homeBackground = [room1, room2]
    app.homeCounter = 0
    app.gameOver = False
    bed1 = app.scaleImage(app.loadImage("sleep1.jpg"), 4)
    bed2 = app.scaleImage(app.loadImage("sleep1.jpg"), 4)
    app.bedSprite = [bed1, bed2]
    app.bedSpriteCounter = 0
    app.fridgeOrder = ["eggs", "meat", "tomatoes", "water", "scallions", "fennel"]
    app.fridgeItems = [app.eggItem, app.meatItem, app.tomatoItem, app.waterItem,
                        app.scallionItem, app.fennelItem]
    app.cabinetOrder = ["flour", "rice", "sugar", "soy sauce", "noodles"]
    app.cabinetItems = [app.flourItem, app.riceItem, app.sugarItem, app.soySauceItem,
                        app.noodlesItem]
    url = "fridge.png"
    spritestrip = app.loadImage(url)
    app.fridgeSprite = []
    for i in range(2):
        sprite = spritestrip.crop((0, 96 * i, 96, 96 * (1 + i)))
        sprite = app.scaleImage(sprite, 3)
        app.fridgeSprite.append(sprite) #append each sprite to array

    url = "home.png"
    app.homeSprite = app.loadImage(url)
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
    app.bedLoc = (1300, 450)
    app.leftEndLoc = (-100, 450)


    #Vars related to tree or nature stuff
    app.treeSpriteCounter = 0
    url = "tree.png"
    spritestrip = app.loadImage(url)
    app.treeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.treeSprite.append(sprite) #append each sprite to array

    url = "appletree.png"
    spritestrip = app.loadImage(url)
    app.appleTreeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.appleTreeSprite.append(sprite) #append each sprite to array
    url = "peachTree.png"
    spritestrip = app.loadImage(url)
    app.peachTreeSprite = []
    for i in range(3):
        sprite = spritestrip.crop((0, 320 * i, 320, 320 * (1 + i)))
        sprite = app.scaleImage(sprite, 0.85)
        app.peachTreeSprite.append(sprite) #append each sprite to array


    url = "grass.png"
    app.grassSprite = app.loadImage(url)
    url = "neutralgrass.png"
    app.neutralGrassSprite = app.loadImage(url)
    url = "anxgrass.png"
    app.anxGrassSprite = app.loadImage(url)
    url = "sadgrass.png"
    app.sadGrassSprite = app.loadImage(url)
    app.skyBackground = app.loadImage("sky.png")
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
    url = "overlay.png"
    app.overlaySprite = app.loadImage(url)
    app.overlaySprite = app.scaleImage(app.overlaySprite, 4)
    url = "flowers1.png"
    url2 = "flowers2.png"
    app.flowerSprite = []
    app.happyFlowerSprite = [app.loadImage(url), app.loadImage(url2)]
    app.flowerSpriteCounter = 0
    app.sadFlowerSprite = [app.loadImage("sadflowers.png"), app.loadImage("sadflowers2.png")]
    app.neutralFlowerSprite = [app.loadImage("neutralflowers.png"), app.loadImage("neutralflowers1.png")]
    app.anxFlowerSprite = [app.loadImage("anxflowers.png"), app.loadImage("anxflowers2.png")]


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
    app.sfx = []
    app.sfx.append(Sound("pickingSound.WAV"))

    app.sound = ""
    if (app.vibe == "happy"):
        app.vibe = app.happyColorDict
        app.sound = Sound("summer.mp3")
        app.timerDelay = 350
        app.flowerSprite = app.happyFlowerSprite

    elif (app.vibe == "sad"):
        app.vibe = app.sadColorDict
        app.sound = Sound("acoustic dream.mp3")
        app.timerDelay = 1200
        app.flowerSprite = app.sadFlowerSprite


    elif (app.vibe == "neutral"):
        app.vibe = app.neutralColorDict
        app.sound = Sound("the golden hour.mp3")
        app.timerDelay = 700
        app.flowerSprite = app.neutralFlowerSprite

    else:
        app.vibe = app.anxColorDict
        app.sound = Sound("the golden hour.mp3")
        app.timerDelay = 150
        app.flowerSprite = app.anxFlowerSprite


    if (app.mode == "homeMode"):
        app.sound = Sound("tides of summer.mp3")

    app.pickingSound = pygame.mixer.Sound("pickupCoin.WAV")  
    app.selectSound = pygame.mixer.Sound("blipSelect.WAV")  
    app.openSound = pygame.mixer.Sound("openSound.WAV")

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

class Icon():
    def __init__(self, name, loc, sprite):
        self.name = name
        self.loc = (loc[0], loc[1])
        self.sprite = sprite
    
    def mouseClickedNear(self, other):
        x, y = self.loc
        return (abs(other.x - x) <= 30 and abs(other.y - y) <= 30)

class Recipe():
    def __init__(self, name, requiredIngredients, sprite):
        self.name = name
        self.ingredients = requiredIngredients
        self.loc = (0, 0)
        self.sprite = sprite

class Item():
    def __init__(self, name, loc, sprite, canEat):
        self.loc = loc
        self.name = name
        self.sprite = sprite
        self.count = 0
        self.canEat = canEat
    
    def eat(self):
        if (self.count > 0):
            self.count -= 1
            return True
        return False
    
    def mouseClickedNear(self, other):
        x, y = self.loc
        return (abs(other.x - x) <= 15 and abs(other.y - y) <= 15)

class Tree():
    def __init__(self, app, row, col):
        self.loc = (row, col)
        self.sprite = app.treeSprite
    
    def mouseClickedNear(self, app, event):
        row, col = self.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        mouseX, mouseY = event.x, event.y
        playerX, playerY = app.playerPos
        return (abs(mouseX - cx) <= 120 and abs(mouseY - cy) <= 120 and
                abs(playerX - cx) <= 250 and abs(playerY - cy) <= 250)

    def getCenter(self, app):
        row, col = self.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        return (cx, cy)


class Plant():
    def __init__(self, app, row, col, sprite):
        self.loc = (row, col)
        self.sprite = sprite
        self.picked = False
        self.name = ""
        if (self.sprite == app.scallionSprite):
            self.name = "scallions"
        else:
            self.name = "fennel"
    
    def getCenter(self, app):
        row, col = self.loc
        x0, y0, x1, y1 = getCellBoundsinCartesianCoords(app, row, col)
        cx, cy = (x1 + x0)/2, (y1 + y0)/2 #get center
        cx, cy = gameMode_2DToIso(app, cx, cy)
        return (cx, cy)


class FruitTree(Tree): #apple or peach tree
    def __init__(self, app, row, col, fruit, sprite):
        super().__init__(app, row, col)
        self.fruitPicked = False
        self.sprite = sprite
        self.fruit = fruit

    def changeTree(self, app):
        if (self.fruitPicked):
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
    r, c = r + 2, c + 1
    return r, c


#returns true if player x, y is within row, col bounds
def homeMode_constraintsMet(app, x):
    x, y = app.playerPos
    return (x > app.leftEndLoc[0])

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
        if (app. displayJournal):
            app.journal.close()
            #change it into reading mode to display text
            app.journal = open("journal.txt", "r")
    if (withinRange(app, event, app.stoveLoc)):
        app.displayStove = True
        pygame.mixer.find_channel().play(app.openSound)
    if (withinRange(app, event, app.fridgeLoc) and not app.displayCabinet):
        app.displayFridge = True
        pygame.mixer.find_channel().play(app.openSound)
    if (withinRange(app, event, app.cabinetLoc) and not app.displayFridge):
        app.displayCabinet = True
        pygame.mixer.find_channel().play(app.openSound)

    if (app.recipeIcon.mouseClickedNear(event)):
        app.displayRecipe = True
        pygame.mixer.find_channel().play(app.openSound)

    elif (app.displayRecipe):
        if (app.closeIcon.mouseClickedNear(event)):
            app.displayRecipe = False
            pygame.mixer.find_channel().play(app.selectSound)

    if (app.inventoryIcon.mouseClickedNear(event)):
        if (app.displayInventory): #is open, so play closing sound
            pygame.mixer.find_channel().play(app.selectSound)

        else:
            pygame.mixer.find_channel().play(app.openSound)

        app.displayInventory = not app.displayInventory


    # if (350 <= event.x <= 450 and 600 <= event.y <= 750):
    #     app.goBed = True
    #     pygame.mixer.find_channel().play(app.openSound)

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
                    print('insufficient ingredients')
                    app.homeText = "insufficient ingredients!"
                    pygame.mixer.find_channel().play(app.selectSound)
                    app.homeTextTimer = 3
                if (canCook):
                    for ingredient in recipeDict: 
                        for item in app.inventoryList:
                            if (ingredient == item.name):
                                item.count -= recipeDict[ingredient]
                        #remove used ingredients
                    print("cooked recipe")
                    app.homeText = f"cooked {recipe.name}!"
                    pygame.mixer.find_channel().play(app.openSound)
                    app.homeTextTimer = 3
                    recipeItem = app.recipeNamesList[f"{recipe.name}"]
                    if (recipeItem not in app.inventoryList):
                        app.inventoryList.append(recipeItem)
                    recipeItem.count += 1
                    

def gameMode_mousePressed(app, event):
    if (app.displayJournal):
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
        app.playerSprite = app.scaleImage(app.playerHomeSprite, 3.7)
        app.goHome = True
        app.timerDelay = 500
        app.sound = Sound("tides of summer.mp3")
        # app.sound.start(loops = -1)
        app.mode = "homeMode"
    else:
        cx, cy = app.playerPos
        playerRow, playerCol = getPlayerRowCol(app, cx, cy)
        for tree in app.treeList:
            # row, col = tree.loc
            # if (abs(row - playerRow) <= 2 and abs(col - playerCol) <= 2 and type(tree) == FruitTree):
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

    elif (dir == "right"):
        if (x >= app.width - app.boundingBoxLimit):
            app.homeX += app.homeCameraOffset
            app.stoveLoc = (app.stoveLoc[0] - app.homeCameraOffset, app.stoveLoc[1])
            app.fridgeLoc = (app.fridgeLoc[0] - app.homeCameraOffset, app.fridgeLoc[1])
            app.cabinetLoc = (app.cabinetLoc[0] - app.homeCameraOffset, app.cabinetLoc[1])
            app.bedLoc = (app.bedLoc[0] - app.homeCameraOffset, app.bedLoc[1])

def homeMode_keyPressed(app, event):
    cx, cy = app.playerPos
    if (app.goBedConfirm):
        if (event.key == "g"):
            app.goBed = True
        else:
            app.goBedConfirm = False
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
        elif (event.key == "n"):
            app.gameOver = True

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
        if (event.key == 'Enter'):
            app.journal.write(app.text + "\n")
            app.text = ""
            app.textLenChecker += 1

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

def changeTreeList(app):
    playerX, playerY = app.playerPos
    for i in range(len(app.treeList)):
        tree = app.treeList[i]
        cx, cy = tree.getCenter(app)
        if (cy <= playerY - 42): #tree is behind player
            app.behindTreeList.append(tree)
            if (tree in app.frontTreeList):
                app.frontTreeList.remove(tree)
        elif (cy >= playerY + 42): #tree is in front of player
            app.frontTreeList.append(tree)
            if (tree in app.behindTreeList):
                app.behindTreeList.remove(tree)

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
    if app.flowerSpriteCounter == 1:
        app.flowerSpriteCounter = 0
    else:
        app.flowerSpriteCounter = 1

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
    print(app.feelingsDict)
    changeColors(app)

def changeColors(app):
    largestMood = "Happy"
    largestMoodCount = 0.0
    for feeling in app.feelingsDict:
        # print(feeling, app.feelingsDict[feeling])
        if app.feelingsDict[feeling] > largestMoodCount:
            largestMood = feeling
            print("changing")
            largestMoodCount = app.feelingsDict[feeling]
    if (largestMood == "Happy"):
        largestMood = "happy"
    elif (largestMood == "Fear" or largestMood == "Surprise"):
        largestMood = "neutral"
    elif (largestMood == "Anger"):
        largestMood = "anx"
    else:
        largestMood = "sad"
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
            chance = random.randint(1, 2) #fill board w scallions and fennel
            # if (chance == 1):
            #     app.plantList.append(Plant(app, row, col, app.scallionSprite))
            # else:
            #     app.plantList.append(Plant(app, row, col, app.fennelSprite))



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
    recipeBook = getCachedPhotoImage(app, app.recipeSprite)
    canvas.create_image(app.width//2, app.height//2, image = recipeBook)
    canvas.create_text(200, 220, text = "journal", 
                        font = f"{app.font} 24 bold", anchor = "s")
    i = 0
    app.journal.seek(0)
    lines = app.journal.readlines()
    for line in lines:
        if (i >= 20): 
            #put on next half of page
            canvas.create_text (600, 250 + (i - 20) * 20, text = line, 
            font = f"{app.font} 12")
        else:
            canvas.create_text (200, 230 + i * 20, text = line, 
            font = f"{app.font} 12")
        i += 1

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

    # hungerStart = 500
    # canvas.create_rectangle(hungerStart, 600, hungerStart + 200, 650, fill = "black")
    # hungerPos = hungerStart + (app.hungerMeter/100) * 200
    # canvas.create_rectangle(hungerStart, 600, hungerPos, 650, fill = "red")


def gameMode_drawTreesInBack(app, canvas):
    # for plant in app.plantList: 
    #     cx, cy = plant.getCenter(app)
    #     if (0 <= cx <= app.width * 2 and 0 <= cy <= app.height * 2):
    #         plant = getCachedPhotoImage(app, plant.sprite)
    #         canvas.create_image(cx, cy - 120, image=plant)

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
    sky = getCachedPhotoImage(app, app.skyBackground)
    canvas.create_image(app.width//2, app.width//2, image=sky)


def homeMode_drawHome(app, canvas):
    canvas.create_rectangle(0, 0, app.height, app.width, fill = "black")
    home = getCachedPhotoImage(app, app.homeBackground[app.homeCounter])
    canvas.create_image(400 - app.homeX, 400, image = home)
    x, y = app.bedLoc
    canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill = "white")


def homeMode_drawText(app, canvas):
    canvas.create_text(app.width//2, 150, text = f"{app.homeText}", 
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
        homeMode_drawText(app, canvas)

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