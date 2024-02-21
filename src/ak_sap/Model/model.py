from pathlib import Path
import typing

from .constants import _UNITS, _UNITS_LITERALS, _PROJECT_INFO_KEYS
from ak_sap.utils import log, MasterClass
from ak_sap.utils.decorators import smooth_sap_do

class Model(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
    
    def __str__(self) -> str:
        return 'Instance of `Model`. Holds collection of model functions'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def units(self) -> _UNITS_LITERALS:
        assert self.SapModel is not None
        """Returns the units presently specified for the model"""
        _units: _UNITS_LITERALS = _UNITS[self.SapModel.GetPresentUnits() - 1]
        log.debug(f'Queried Units: {_units}')
        return _units
    
    @property
    def units_database(self) -> _UNITS_LITERALS:
        """Returns the database units for the model. 
        All data is internally stored in the model in these units and 
        converted to the present units as needed."""
        assert self.SapModel is not None
        _units: _UNITS_LITERALS = _UNITS[self.SapModel.GetDatabaseUnits() - 1]
        log.debug(f'Queried Database Units: {_units}')
        return _units
    
    @smooth_sap_do
    def set_units(self, value: _UNITS_LITERALS):
        """Updates the current units of model"""
        assert self.SapModel is not None
        log.info(f'Updating the current units to {value}')
        _unit_to_set = _UNITS.index(value) + 1
        return self.SapModel.SetPresentUnits(_unit_to_set)

        
    @property
    def merge_tol(self) -> float:
        """Retrieves the value of the program auto merge tolerance"""
        assert self.SapModel is not None
        log.debug('Quering auto-merge tolerance')
        tol, ret = self.SapModel.GetMergeTol()
        try:
            assert ret == 0
        except Exception as e:
            log.critical(str(e) + f'Return Tol: {tol}')
        return tol
    
    @smooth_sap_do
    def set_merge_tol(self, value: float):
        """Sets the program auto merge tolerance"""
        assert self.SapModel is not None
        log.info(f'Updating the auto-merge tolerance to {value}')
        return self.SapModel.SetMergeTol(value)
    
    @property
    def filepath(self) -> Path:
        """Returns full path where the file is located"""
        assert self.SapModel is not None
        log.debug('Quering the filepath of active model.')
        try:
            path = Path(self.SapModel.GetModelFilename())
            log.debug(path)
            return path
        except Exception as e:
            log.critical(str(e))
            return Path()
        
    @property
    def is_locked(self) -> bool:
        assert self.SapModel is not None
        """Returns True if the model is locked and False if it is unlocked."""
        return self.SapModel.GetModelIsLocked()
    
    @property
    def project_info(self) -> dict:
        """retrieves the project information data."""
        assert self.SapModel is not None
        info = {x: "" for x in typing.get_args(_PROJECT_INFO_KEYS)}
        _items, keys, values, ret = self.SapModel.GetProjectInfo()
        try:
            assert ret == 0
            for k, v in zip(keys, values):
                info[k] = v
        except Exception as e:
            log.critical(str(e) + f'Return values: \n{_items=}\n{keys=}\n{values=}')
        return info
    
    def set_project_info(self, value: dict):
        """sets the data for an item in the project information."""
        assert self.SapModel is not None
        log.info(f'Setting project info to {value}')
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
        assert self.SapModel is not None
        log.debug('Extracting Sap logs')
        return self.SapModel.GetUserComment()[0]
    
    @smooth_sap_do
    def set_logs(self, value: str) -> None:
        """sets the user comments and log data."""
        assert self.SapModel is not None
        return self.SapModel.SetUserComment(value)

    def lock(self):
        """Lock Model"""
        self.__update_lock(lock=True)
    
    def unlock(self):
        """Unlock Model"""
        self.__update_lock(lock=False)
        
    def __update_lock(self, lock: bool):
        """Lock/Unlock Model"""
        assert self.SapModel is not None
        try:
            assert self.SapModel.SetModelIsLocked(lock) == 0
            log.info(f'Model Lock status set to `{lock}`')
        except Exception as e:
            log.critical(str(e))
    
    def refresh(self):
        """ refreshes the view for the windows"""
        assert self.SapModel is not None
        try:
            assert self.SapModel.View.RefreshView() == 0
            log.debug('Model refreshed')
        except Exception as e:
            log.critical(str(e))
        