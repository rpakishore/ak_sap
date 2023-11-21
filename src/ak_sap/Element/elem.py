from .point import Point

class Element:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        
        self.Point = Point(mySapObject=mySapObject)