from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

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
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)
     
class Drone(GameConstruct):
    
    droneCount = 0
    
    def __init__(self,
                 nodeName: str, 
                 loader: Loader, parentNode: NodePath,  
                 modelPath: str, texPath: str, 
                 posVec: Vec3, hpr: Vec3, scaleVec: float):
        
        super().__init__(nodeName, loader, parentNode, modelPath, texPath, posVec, hpr, scaleVec)

        