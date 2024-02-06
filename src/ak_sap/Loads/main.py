from .LoadCases import LoadCase
from .LoadPatterns import LoadPattern

class Load:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        
        #Definition of Submodules
        self.Pattern = LoadPattern(mySapObject=mySapObject)
        self.Case = LoadCase(mySapObject=mySapObject)