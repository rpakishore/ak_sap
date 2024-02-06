import typing

from .constants import LoadCases
from ak_sap.utils.decorators import smooth_sap_do

class LoadCase:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return 'Instance of `LoadCase`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        """returns the number of defined load patterns."""
        return self.total()
    
    @smooth_sap_do
    def total(self, casetype: LoadCases|None = None):
        """returns the total number of defined load cases in the model. 
        If desired, counts can be returned for all load cases of a specified type in the model."""
        if casetype is None:
            return self.SapModel.LoadCases.Count()
        else:
            _value = typing.get_args(LoadCases).index(casetype) + 1
            return self.SapModel.LoadCases.Count(_value)