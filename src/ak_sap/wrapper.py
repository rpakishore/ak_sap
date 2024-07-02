import comtypes.client

from pathlib import Path
import sys

from ak_sap.Analyze import Analyze
from ak_sap.Database import Table
from ak_sap.Loads import Load
from ak_sap.Material.material import Material
from ak_sap.Model import Model
from ak_sap.Object import Object
from ak_sap.Results import Results
from ak_sap.Select import Select
from ak_sap.utils.logger import log

_known_program_paths: list[str] = [
    r"C:\Program Files\Computers and Structures\SAP2000 24\SAP2000.exe",
    r"C:\Program Files\Computers and Structures\SAP2000 21\SAP2000.exe"
]

class Sap2000Wrapper:
    def __init__(self, attach_to_exist: bool = True, program_path: str|Path|None = None) -> None:
        self.attach_to_exist: bool = attach_to_exist
        self.program_path: str|None=  str(Path(str(program_path)).absolute()) if program_path else None
        self.mySapObject = model(attach_to_instance=attach_to_exist, program_path=program_path)
        self.SapModel = self.mySapObject.SapModel
        
        #Attach submodules and functions
        self.Analyze = Analyze(mySapObject=self.mySapObject)
        self.Model = Model(mySapObject=self.mySapObject)
        self.Object = Object(mySapObject=self.mySapObject)
        self.Table = Table(mySapObject=self.mySapObject, Model=self.Model)
        self.Load = Load(mySapObject=self.mySapObject)
        self.Results = Results(mySapObject=self.mySapObject)
        self.Material = Material(mySapObject=self.mySapObject)
        self.Select = Select(mySapObject=self.mySapObject)
        
        log.info('Sap2000Wrapper Initialized')
    
    def __str__(self) -> str:
        _attachment_str = 'Attached to existing Model' if self.attach_to_exist else 'New Model'
        return f'Instance of SAP2000Wrapper. Model type: "{_attachment_str}".'
    
    def __repr__(self) -> str:
        attach_to_exist = self.attach_to_exist
        return f'Sap2000Wrapper({attach_to_exist=})'
    
    def __del__(self) -> None:
        try:
            # assert self.mySapObject.ApplicationExit(False) == 0
            self.SapModel = None
            self.mySapObject = None
        except Exception as e:
            log.error(e.__str__())
    
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
            self.mySapObject.Hide() 
            return True
        except Exception as e:
            log.critical(str(e))
            return False
    
    def unhide(self) -> bool:
        """Unhides the Sap2000 application. 
        When hidden it is not visible on the screen or on the Windows task bar.
        """
        try:
            self.mySapObject.Unhide()
            return True
        except Exception as e:
            log.critical(str(e))
            return False
    
    @property
    def ishidden(self) -> bool:
        return self.mySapObject.Visible()
    
    @property
    def version(self) -> str:
        return self.SapModel.GetVersion()[0]
    
    def exit(self, save: bool=False):
        self.mySapObject.ApplicationExit(False)
        
def model(attach_to_instance: bool, program_path: str|Path|None = None,
            known_program_paths: list[str] = _known_program_paths):
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
    else:
        if program_path is None:
            for filepath in known_program_paths:
                if Path(filepath).is_file():
                    program_path = filepath
                    break
        assert program_path is not None, 'SAP2000.exe file not found. Please pass the program_path to initialize instance'

        try:
            mySapObject = helper.CreateObject(program_path)
            mySapObject.ApplicationStart()
            mySapObject.SapModel.InitializeNewModel()   #initialize model
            log.debug(f'Created model from {program_path}.')
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("Cannot start a new instance of the program.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)
