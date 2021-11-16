from cmu_112_graphics import *
import math
import random

#how to make clouds
#an array of circles
#list stores the centers of all the circles
#the circles are concentrated in the 'middle" . loool uh
#each timerfired, remove first circle
#add a circle at the end
#ok how about
#make each cloud have a "range"
#when you generate the cloud, make it concentrated in the middle
#bruh idk how though
#randx, randy
#use sech function middle is 0, two outer ends has less stuff.. 
#math.acosh(x)
#scale it by that?? multiply the randx value by acosh,
#so if its at the outer ends it will go down
#if its in the middle it will go up
#if its below a certain cap dont draw it
#actually i can just.. use the sech function and change the vars.. 

def appStarted(app):
    app.circleList = []
    app.cloudLength = 10
    app.timerDelay = 1000
    generateCloud(app)

def generateCloud(app):
    for x in range(-100, 100, 10):
        y = 1/(math.cosh(x//6)) * 20
        y += random.randint(-10, 10)
        app.circleList.append((x + 200, y + 200))

def timerFired(app):
    #move every element in cloud to right
    newCircleList = []
    yOffset = random.randint(-10, 10)
    for x, y in app.circleList:
        newCircleList.append((x + 3, y + yOffset))
    app.circleList = newCircleList

def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0 , 400, 400, fill = "blue")
    for i in range(len(app.circleList)):
        x, y = app.circleList[i]
        x = x % 400
        y = 400 - y #flip it cuz coords suck
        #change r by whether its at beginning, middle, or end
        #ex if i = 0, then r gives a smaller value since math.sech(-5)
        rdm = 1.5
        r = (1/(math.cosh((i - 10)//rdm))) * 10
        if (r >= 0.5):
            canvas.create_oval(x - r, y - (rdm * r), x + (1.1 * r), y + r, fill = "white",
                            width = 0)

runApp(width = 400, height = 400)