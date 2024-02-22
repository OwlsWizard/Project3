from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task

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
        
        self.accept("q", self.leftRoll, [1])
        self.accept("q-up", self.leftRoll, [0])
            
    def thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyThrust, "forward-thrust")
        else:
            self.taskManager.remove("forward-thrust")
            
    def leftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyLeftTurn, "left-turn")
        else:
            self.taskManager.remove("left-turn")
    
    def rightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyRightTurn, "right-turn")
        else:
            self.taskManager.remove("right-turn")    

    def upTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyUpTurn, "up-turn")
        else:
            self.taskManager.remove("up-turn")
    
    def downTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyDownTurn, "down-turn")
        else:
            self.taskManager.remove("down-turn")
            
    def leftRoll(self, keyDown):
        if keyDown:
            self.taskManager.add(self.applyleftRoll, "left-roll")
        else:
            self.taskManager.remove("left-roll")                   
                
    def applyThrust(self, task):
        shipSpeed = 5 #rate of movement
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward()) #Pulls direction ship is facing
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * shipSpeed) #controls movement itself
        return Task.cont
    
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

    def applyleftRoll(self, task): 
        """
        FIXME: Other directions after turn are turning relative to the world, not the model.
        Likely because the model itself is moving due to absolute coordinates, and not relative coordinates.
        check for getHPR method, and calc based off of sin/cos?
        """
        
        self.modelNode.setR(self.modelNode.getR() + self.turnRate)
        return Task.cont
     
class Drone(GameConstruct):
    
    droneCount = 0
    
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)

        