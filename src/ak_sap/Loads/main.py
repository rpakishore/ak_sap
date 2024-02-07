from .LoadCases import LoadCase
from .LoadPatterns import LoadPattern
from .Modal import Modal

class Load:
    def __init__(self, mySapObject) -> None:       
        #Definition of Submodules
        self.Pattern = LoadPattern(mySapObject=mySapObject)
        self.Case = LoadCase(mySapObject=mySapObject)
        self.Modal = Modal(mySapObject=mySapObject)