import comtypes.client

from pathlib import Path
import sys
import typing

from .constants import _UNITS, _UNITS_LITERALS, _PROJECT_INFO_KEYS
from ak_sap.utils import log, ic
ic.configureOutput(prefix=f'{Path(__file__).name} -> ')

class Model:
    def __init__(self, mySapObject) -> None:
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
    
    def __str__(self) -> str:
        return 'Instance of `Model`. Holds collection of model functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def units(self) -> _UNITS_LITERALS:
        """Returns the units presently specified for the model"""
        return _UNITS[self.SapModel.GetPresentUnits() - 1]
    
    @property
    def units_database(self) -> _UNITS_LITERALS:
        """Returns the database units for the model. 
        All data is internally stored in the model in these units and 
        converted to the present units as needed."""
        return _UNITS[self.SapModel.GetDatabaseUnits() - 1]
    
    def set_units(self, value: _UNITS_LITERALS):
        """Updates the current units of model"""
        try:
            _unit_to_set = _UNITS.index(value) + 1
            assert self.SapModel.SetPresentUnits(_unit_to_set) == 0
        except Exception as e:
            log.critical(str(e))
        
    @property
    def merge_tol(self) -> float:
        """Retrieves the value of the program auto merge tolerance"""
        return self.SapModel.GetMergeTol()[0]
    
    def set_merge_tol(self, value: float):
        """Sets the program auto merge tolerance"""
        try:
            assert self.SapModel.SetMergeTol(value) == 0
        except Exception as e:
            log.critical(str(e))
    
    @property
    def filepath(self) -> Path:
        """Returns full path where the file is located"""
        return Path(self.SapModel.GetModelFilename())
    
    @property
    def is_locked(self) -> bool:
        """Returns True if the model is locked and False if it is unlocked."""
        return self.SapModel.GetModelIsLocked()
    
    @property
    def project_info(self) -> dict:
        """retrieves the project information data."""
        info = {x: "" for x in typing.get_args(_PROJECT_INFO_KEYS)}
        for k, v in zip(self.SapModel.GetProjectInfo()[1], self.SapModel.GetProjectInfo()[2]):
            info[k] = v
        return info
    
    def set_project_info(self, value: dict):
        """sets the data for an item in the project information."""
        allowable_keys = typing.get_args(_PROJECT_INFO_KEYS)
        try:
            for k, v in value.items():
                assert k in allowable_keys
                assert self.SapModel.SetProjectInfo(k, v) == 0
        except Exception as e:
            log.critical(str(e))
    
    @property
    def logs(self) -> str:
        """retrieves the data in the user comments and log."""
        return self.SapModel.GetUserComment()[0]
    
    def set_logs(self, value: str) -> None:
        """sets the user comments and log data."""
        try:
            assert self.SapModel.SetUserComment(value) == 0
        except Exception as e:
            log.critical(str(e))
            
    def lock(self):
        self._update_lock(lock=True)
    
    def unlock(self):
        self._update_lock(lock=False)
        
    def _update_lock(self, lock: bool):
        try:
            assert self.SapModel.SetModelIsLocked(lock) == 0
        except Exception as e:
            log.critical(str(e))