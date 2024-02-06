import typing

from .constants import LoadPatterns
from ak_sap.utils.decorators import smooth_sap_do

class LoadPattern:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return 'Instance of `LoadPattern`. Holds collection of functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        """returns the number of defined load patterns."""
        return self.SapModel.LoadPatterns.Count()
    
    @smooth_sap_do
    def add(self, name: str, pattern_type: LoadPatterns, 
            selfwt_multiplier: float=0, add_case: bool=False):
        """adds a new load pattern."""
        chosen_pattern = typing.get_args(LoadPatterns).index(pattern_type) + 1
        return self.SapModel.LoadPatterns.Add(name, chosen_pattern, 
                                                selfwt_multiplier, add_case)

    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """applies a new name to a load pattern."""
        return self.SapModel.LoadPatterns.ChangeName(old_name, new_name)

    @smooth_sap_do
    def delete(self, name: str):
        """deletes the specified load pattern."""
        return self.SapModel.LoadPatterns.Delete(name)

    @smooth_sap_do
    def set_loadtype(self, name: str, pattern_type: LoadPatterns):
        """assigns a load type to a load pattern."""
        chosen_pattern = typing.get_args(LoadPatterns).index(pattern_type) + 1
        return self.SapModel.LoadPatterns.SetLoadType(name, chosen_pattern)

    @smooth_sap_do
    def get_loadtype(self, name: str) -> str:
        """assigns a load type to a load pattern."""
        value = self.SapModel.LoadPatterns.GetLoadType(name)
        chosen_pattern = typing.get_args(LoadPatterns)[value[0] - 1]
        return chosen_pattern, 0 # type: ignore

    @smooth_sap_do
    def set_selfwt_multiplier(self, name: str, selfwt_multiplier: float):
        return self.SapModel.LoadPatterns.SetSelfWtMultiplier(name, selfwt_multiplier)

    @smooth_sap_do
    def get_selfwt_multiplier(self, name: str) -> float:
        return self.SapModel.LoadPatterns.GetSelfWtMultiplier(name)
    
    @smooth_sap_do
    def list(self) -> tuple[str]:
        values = self.SapModel.LoadPatterns.GetNameList()
        return values[1:]