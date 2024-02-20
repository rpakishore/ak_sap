from .LoadCases import LoadCase
from .LoadPatterns import LoadPattern
from .LoadCombos import LoadCombo
from .Modal import Modal

class Load:
    def __init__(self, mySapObject) -> None:       
        #Definition of Submodules
        self.Pattern = LoadPattern(mySapObject=mySapObject)
        self.Case = LoadCase(mySapObject=mySapObject)
        self.Combo = LoadCombo(mySapObject=mySapObject)
        self.Modal = Modal(mySapObject=mySapObject)