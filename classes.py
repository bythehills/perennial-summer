import pygame
from helper import *

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
        return (abs(other.x - x) <= 50 and abs(other.y - y) <= 50)

class Tree():
    def __init__(self, app, row, col):
        self.loc = (row, col)
        self.sprite = app.treeSprite
        self.isFront = False
    
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

