import comtypes.client

from pathlib import Path
import sys

from .constants import _UNITS, _UNIT_TYPES
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
    def units(self) -> _UNIT_TYPES:
        """Returns the units presently specified for the model"""
        return _UNITS[self.SapModel.GetPresentUnits() - 1]
    
    @property
    def units_database(self) -> _UNIT_TYPES:
        """Returns the database units for the model. 
        All data is internally stored in the model in these units and 
        converted to the present units as needed."""
        return _UNITS[self.SapModel.GetDatabaseUnits() - 1]
    
    def set_units(self, value: _UNIT_TYPES):
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