from .Eigen.main import Eigen
from .Ritz.main import Ritz
from .TimeHistoryLinear.main import TimeHistoryLinear
from .TimeHistoryNonlinear.main import TimeHistoryNonlinear

class Modal:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        
        #Subclasses
        self.Eigen = Eigen(mySapObject=mySapObject)
        self.Ritz = Ritz(mySapObject=mySapObject)
        self.TimeHistoryLinear = TimeHistoryLinear(mySapObject=mySapObject)
        self.TimeHistoryNonlinear = TimeHistoryNonlinear(mySapObject=mySapObject)
        
    def __str__(self) -> str:
        return 'Instance of `Loads.Modal`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    