import typing

from .constants import LoadPatternType
from ak_sap.utils import MasterClass
from ak_sap.utils.decorators import smooth_sap_do

class LoadPattern(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        self.LoadPatterns = mySapObject.SapModel.LoadPatterns
    
    def __str__(self) -> str:
        return 'Instance of `LoadPattern`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        """returns the number of defined load patterns."""
        return self.LoadPatterns.Count()
    
    @smooth_sap_do
    def add(self, name: str, pattern_type: LoadPatternType, 
            selfwt_multiplier: float=0, add_case: bool=False):
        """adds a new load pattern."""
        chosen_pattern = typing.get_args(LoadPatternType).index(pattern_type) + 1
        return self.LoadPatterns.Add(name, chosen_pattern, 
                                                selfwt_multiplier, add_case)

    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """applies a new name to a load pattern."""
        return self.LoadPatterns.ChangeName(old_name, new_name)

    @smooth_sap_do
    def delete(self, name: str):
        """deletes the specified load pattern."""
        return self.LoadPatterns.Delete(name)

    @smooth_sap_do
    def set_loadtype(self, name: str, pattern_type: LoadPatternType):
        """assigns a load type to a load pattern."""
        chosen_pattern = typing.get_args(LoadPatternType).index(pattern_type) + 1
        return self.LoadPatterns.SetLoadType(name, chosen_pattern)

    @smooth_sap_do
    def get_loadtype(self, name: str) -> str:
        """assigns a load type to a load pattern."""
        value = self.LoadPatterns.GetLoadType(name)
        chosen_pattern = typing.get_args(LoadPatternType)[value[0] - 1]
        return chosen_pattern, 0 # type: ignore

    @smooth_sap_do
    def set_selfwt_multiplier(self, name: str, selfwt_multiplier: float):
        return self.LoadPatterns.SetSelfWtMultiplier(name, selfwt_multiplier)

    @smooth_sap_do
    def get_selfwt_multiplier(self, name: str) -> float:
        return self.LoadPatterns.GetSelfWtMultiplier(name)
    
    @smooth_sap_do
    def list_all(self) -> tuple[str]:
        values = self.LoadPatterns.GetNameList()
        return values[1:]