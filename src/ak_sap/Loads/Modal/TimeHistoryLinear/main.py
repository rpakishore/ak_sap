class TimeHistoryLinear:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return f'Instance of `Loads.Modal.{self.__class__.__name__}`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()