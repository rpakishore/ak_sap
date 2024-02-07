from .Eigen.main import Eigen
from .Ritz.main import Ritz

class Modal:
    def __init__(self, mySapObject) -> None:
        #Subclasses
        self.Eigen = Eigen(mySapObject=mySapObject)
        self.Ritz = Ritz(mySapObject=mySapObject)
        
    def __str__(self) -> str:
        return 'Instance of `Loads.Modal`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()