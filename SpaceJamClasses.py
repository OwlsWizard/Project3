from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task

import math

class GameConstruct(ShowBase):
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        
        self.modelNode.setName(nodeName)
        self.modelNode.setTexture(loader.loadTexture(texPath), 1)
        
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(hpr) 
        self.modelNode.setScale(scaleVec)    

class Universe(GameConstruct):
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):

        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)

class Planet(GameConstruct):
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)
    
class SpaceStation(GameConstruct):
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)

class Player(GameConstruct):
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float,
                 taskMgr: Task, renderer: NodePath):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)
        self.taskManager = taskMgr
        self.render = renderer
        
        self.turnRate = 0.5
        self.setKeybinds()

    def setKeybinds(self):
        self.accept("space", self.thrust, [1])
        self.accept("space-up", self.thrust, [0])
        
        self.accept("a", self.leftTurn, [1])
        self.accept("a-up", self.leftTurn, [0])
        
        self.accept("d", self.rightTurn, [1])
        self.accept("d-up", self.rightTurn, [0])
        
        self.accept("w", self.upTurn, [1])
        self.accept("w-up", self.upTurn, [0])

        self.accept("s", self.downTurn, [1])
        self.accept("s-up", self.downTurn, [0])
        
        self.accept("arrow_left", self.leftRoll, [1])
        self.accept("arrow_left-up", self.leftRoll, [0])

        self.accept("arrow_right", self.rightRoll, [1])
        self.accept("arrow_right-up", self.rightRoll, [0])
             
    def thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyThrust, "forward-thrust")
        else:
            self.taskManager.remove("forward-thrust")
            
    def leftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyLeftTurnTest, "left-turn")
        else:
            self.taskManager.remove("left-turn")
            print(self.modelNode.getHpr())
    
    def rightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyRightTurnTest, "right-turn")
        else:
            self.taskManager.remove("right-turn")
            print(self.modelNode.getHpr())    

    def upTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyUpTurnTest, "up-turn")
        else:
            self.taskManager.remove("up-turn")
            print(self.modelNode.getHpr())
    
    def downTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyDownTurnTest, "down-turn")
        else:
            self.taskManager.remove("down-turn")
            print(self.modelNode.getHpr())
            
    def leftRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyLeftRoll, "left-roll")
        else:
            self.taskManager.remove("left-roll")
            print(self.modelNode.getHpr())                   

    def rightRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyRightRoll, "right-roll")
        else:
            self.taskManager.remove("right-roll")
            print(self.modelNode.getHpr())    
                
    def applyThrust(self, task):
        shipSpeed = 5 #rate of movement
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward()) #Pulls direction ship is facing
        """
        FIXME: If trajectory is set to self.modelNode, then the ship will fly forward regardless of the direction the camera is facing.
        """
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * shipSpeed) #controls movement itself
        return Task.cont

    def pullVectorLR(self, hpr: Vec3):
        """
        Pulls actual vector to increase in movement direction for left, right movement. 
        Needed to fix movement issues where tilting "left" tilts ship left relative to world, not model
        """
        rotation = hpr[2]
        relativeX = self.turnRate * math.cos(math.radians(rotation))
        relativeY = self.turnRate * math.sin(math.radians(rotation))
        
        return Vec3(relativeX, relativeY, 0)
    
    def pullVectorUD(self, hpr: Vec3):
        """
        Pulls actual vector to increase in movement direction for Up, Down movement. 
        Needed to fix movement issues where tilting "up" tilts ship up relative to world, not model
        """
        rotation = hpr[2] + 90
        relativeX = self.turnRate * math.cos(math.radians(rotation))
        relativeY = self.turnRate * math.sin(math.radians(rotation))
        
        return Vec3(relativeX, relativeY, 0)
    
    def applyLeftTurnTest(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorLR(rotation)
        vectorx = vector[0]
        vectory = vector[1]
        self.modelNode.setHpr(self.modelNode.getH() + vectorx, self.modelNode.getP() + vectory, self.modelNode.getR())
        return Task.cont    
    
    def applyRightTurnTest(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorLR(rotation)
        vectorx = vector[0]
        vectory = vector[1]
        self.modelNode.setHpr(self.modelNode.getH() - vectorx, self.modelNode.getP() - vectory, self.modelNode.getR())
        return Task.cont    

    def applyUpTurnTest(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorUD(rotation)
        vectorx = vector[0] 
        vectory = vector[1] 
        self.modelNode.setHpr(self.modelNode.getH() + vectorx, self.modelNode.getP() + vectory, self.modelNode.getR())
        return Task.cont   

    def applyDownTurnTest(self, task):
        rotation = self.modelNode.getHpr()
        vector = self.pullVectorUD(rotation)
        vectorx = vector[0] 
        vectory = vector[1] 
        self.modelNode.setHpr(self.modelNode.getH() - vectorx, self.modelNode.getP() - vectory, self.modelNode.getR())
        return Task.cont   

    def applyLeftRoll(self, task): 
        self.modelNode.setR(self.modelNode.getR() + -self.turnRate)
        return Task.cont

    def applyRightRoll(self, task): 
        self.modelNode.setR(self.modelNode.getR() + self.turnRate)
        return Task.cont
    
    """
    def applyLeftTurn(self, task):
        self.modelNode.setH(self.modelNode.getH() + self.turnRate)
        return Task.cont
    
    def applyRightTurn(self, task):
        self.modelNode.setH(self.modelNode.getH() + -self.turnRate)
        return Task.cont
    
    def applyUpTurn(self, task):
        self.modelNode.setP(self.modelNode.getP() + self.turnRate)
        return Task.cont
  
    def applyDownTurn(self, task):
        self.modelNode.setP(self.modelNode.getP() + -self.turnRate)
        return Task.cont      
    """
    
class Drone(GameConstruct):
    
    droneCount = 0
    
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)

        