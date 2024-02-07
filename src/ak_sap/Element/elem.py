from .point import Point

class Element:
    def __init__(self, mySapObject) -> None:       
        self.Point = Point(mySapObject=mySapObject)