from .logger import log

class MasterClass:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        print(f'`{self.__class__.__name__}` instance initialized.')
    
    def __str__(self) -> str:
        return f'Instance of `Loads.Modal.{self.__class__.__name__}`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __del__(self) -> None:
        try:
            self.mySapObject = None
            self.SapModel = None
        except Exception as e:
            log.warning(msg=f'Exception faced when deleting {self.__class__.__name__}\n{e}')