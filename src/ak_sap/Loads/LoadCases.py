import typing

from .constants import LoadCaseType, LoadPatternType
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
    def total(self, casetype: LoadCaseType|None = None):
        """returns the total number of defined load cases in the model. 
        If desired, counts can be returned for all load cases of a specified type in the model."""
        if casetype is None:
            return self.SapModel.LoadCases.Count()
        else:
            _value = typing.get_args(LoadCaseType).index(casetype) + 1
            return self.SapModel.LoadCases.Count(_value)
    
    @smooth_sap_do
    def rename(self, old_name: str, new_name: str):
        """changes the name of an existing load case."""
        assert old_name in self.list_all(), f'"{old_name}" is not in list of defined load cases {self.list_all()}'
        return self.SapModel.LoadCases.ChangeName(old_name, new_name)
    
    @smooth_sap_do
    def list_all(self) -> tuple[str]:
        """retrieves the names of all defined load cases of the specified type."""
        _ret = self.SapModel.LoadCases.GetNameList_1()
        return _ret[1:]
    
    @smooth_sap_do
    def delete(self, name: str):
        assert name in self.list_all(), f'"{name}" is not in list of defined load cases {self.list_all()}'
        return self.SapModel.LoadCases.Delete(name)
    
    @smooth_sap_do
    def case_info(self, name: str) -> dict:
        _ret = self.SapModel.LoadCases.GetTypeOAPI_2(name)
        _value = {
            'CaseType': typing.get_args(LoadCaseType)[_ret[0]-1],
            'DesignType': typing.get_args(LoadPatternType)[_ret[2]-1],
            'DesignTypeOption': 'Program determined' if _ret[3] == 0 else 'User specified',
            'AutoCreated': True if _ret[4] == 1 else False
        }
        
        if _value['CaseType'] == 'MODAL':
            _value['SubType'] = 'Eigen' if _ret[1] == 1 else 'Ritz'
        elif _value['CaseType'] == 'LINEAR_HISTORY':
            _value['SubType'] = 'Transient' if _ret[1] == 1 else 'Periodic'
        else:
            _value['SubType'] = None
        return (_value, 0) # type: ignore
    
    @smooth_sap_do
    def set_type(self, name: str, casetype: LoadCaseType):
        assert name in self.list_all(), f'"{name}" is not in list of defined load cases {self.list_all()}'
        _value = typing.get_args(LoadCaseType).index(casetype) + 1
        return self.SapModel.LoadCases.SetDesignType(name, 1, _value)