import comtypes.client

from pathlib import Path
import sys
from typing import Any

from ak_sap.Model import Model
from ak_sap.Element import Element
from ak_sap.utils.logger import log, ic
ic.configureOutput(prefix=f'{Path(__file__).name} -> ')

class Sap2000Wrapper:
    def __init__(self, attach_to_exist: bool = True, program_path: str|Path|None = None) -> None:
        self.attach_to_exist: bool = attach_to_exist
        self.program_path: str|None=  str(Path(str(program_path)).absolute()) if program_path else None
        self.mySapObject = model(attach_to_instance=attach_to_exist, program_path=program_path)
        self.SapModel = self.mySapObject.SapModel
        
        #Attach submodules and functions
        self.Model = Model(mySapObject=self.mySapObject)
        self.Element = Element(mySapObject=self.mySapObject)
        
        log.info('Sap2000Wrapper Initialized')
    
    def __str__(self) -> str:
        _attachment_str = 'Attached to existing Model' if self.attach_to_exist else 'New Model'
        return f'Instance of SAP2000Wrapper. Model type: "{_attachment_str}".'
    
    def __repr__(self) -> str:
        attach_to_exist = self.attach_to_exist
        return f'Sap2000Wrapper({attach_to_exist=})'
    
    def __del__(self) -> None:
        try:
            assert self.mySapObject.ApplicationExit(False) == 0
            self.SapModel = None
            self.mySapObject = None
            
        except Exception as e:
            log.error(e)
    
    def save(self, savepath: str|Path|None = None) -> bool:
        """Saves SAP model to the `savepath`.
        If no save path is provided, saves to the default path
        """
        try:
            if savepath:
                assert self.SapModel.File.Save(savepath) == 0
                log.info(f'Save success. Saved to {savepath}')
            else:
                assert self.SapModel.File.Save() == 0
                log.info('Save success. Saved to defaultpath')
            return True
        except Exception as e:
            log.critical(e)
            return False
    
    @property
    def api_version(self) -> str:
        """Retrieves the API version implemented by SAP2000."""
        return self.mySapObject.GetOAPIVersionNumber()
    
    def hide(self) -> bool:
        """Hides the Sap2000 application. 
        When hidden it is not visible on the screen or on the Windows task bar.
        """
        try:
            assert self.mySapObject.Hide == 0
            return True
        except Exception as e:
            log.critical(str(e))
            return False
    
    def unhide(self) -> bool:
        """Unhides the Sap2000 application. 
        When hidden it is not visible on the screen or on the Windows task bar.
        """
        try:
            assert self.mySapObject.Unhide == 0
            return True
        except Exception as e:
            log.critical(str(e))
            return False
    
    @property
    def version(self) -> str:
        return self.SapModel.GetVersion()[0]
        
def model(attach_to_instance: bool, program_path: str|Path|None = None):
    """Returns SapObject.
    If `attach_to_instance` is True, returns the current opened model
    If `program_path` is NOT set, Creates a model from latest installed version of SAP2000
    `program_path`, allows lauch of older versions of SAP2000"""
    #create API helper object
    helper = comtypes.client.CreateObject('SAP2000v1.Helper')
    helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
    
    if attach_to_instance:
        #attach to a running instance of SAP2000
        try:
            #get the active SapObject
            mySapObject = helper.GetObject("CSI.SAP2000.API.SapObject") 
            log.debug('Attached to existing Instance.')
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("No running instance of the program found or failed to attach.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)
    elif program_path:
        try:
            mySapObject = helper.CreateObject(program_path)
            mySapObject.ApplicationStart
            mySapObject.SapModel.InitializeNewModel()   #initialize model
            mySapObject.SapModel.File.NewBlank()        #Create new blank model
            log.debug(f'Created model from {program_path}. Initialized and created new blank model')
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("Cannot start a new instance of the program.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)
    else:
        try:
            #create an instance of the SAPObject from the latest installed SAP2000
            mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
            mySapObject.ApplicationStart
            mySapObject.SapModel.InitializeNewModel()   #initialize model
            mySapObject.SapModel.File.NewBlank()        #Create new blank model
            log.debug('Initialized and created new blank model')
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("Cannot start a new instance of the program.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)