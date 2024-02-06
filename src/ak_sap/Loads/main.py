from .LoadCases import LoadCase
from .LoadPatterns import LoadPattern
from .Modal import Modal

class Load:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        
        #Definition of Submodules
        self.Pattern = LoadPattern(mySapObject=mySapObject)
        self.Case = LoadCase(mySapObject=mySapObject)
        self.Modal = Modal(mySapObject=mySapObject)