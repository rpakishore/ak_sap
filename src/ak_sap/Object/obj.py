from .point import Point
from .frame import Frame

class Object:
    def __init__(self, mySapObject) -> None:       
        self.Point = Point(mySapObject=mySapObject)
        self.Frame = Frame(mySapObject=mySapObject)