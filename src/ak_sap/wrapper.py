import sys
from pathlib import Path

import comtypes.client
import pythoncom

from ak_sap.Analyze import Analyze
from ak_sap.Database import Table
from ak_sap.Loads import Load
from ak_sap.Material.material import Material
from ak_sap.Model import Model
from ak_sap.Object import Object
from ak_sap.Results import Results
from ak_sap.Select import Select
from ak_sap.utils.logger import log

# Initialize COM


class Sap2000Wrapper:
    """Wrapper for SAP2000 API.

    This class provides an interface to interact with the SAP2000 program
    through its API, allowing easy manipulation of models, materials,
    loads, results, and more.

    Attributes:
        attach_to_exist (bool): Indicator of whether to attach to an existing instance.
        program_path (str | Path | None): Path to the SAP2000 executable.
        mySapObject: The main SAP2000 object.
        SapModel: The SAP2000 model object.
        Analyze (Analyze): Module for analysis-related functions.
        Model (Model): Module for model-related functions.
        Object (Object): Module for object-related functions.
        Table (Table): Module for database table-related functions.
        Load (Load): Module for load management.
        Results (Results): Module for accessing results.
        Material (Material): Module for managing materials.
        Select (Select): Module for selection functions.
    """

    def __init__(
        self, attach_to_exist: bool = True, program_path: str | Path | None = None
    ) -> None:
        """Initializes the Sap2000Wrapper.

        Args:
            attach_to_exist (bool): If True, attach to an existing instance of SAP2000.
            program_path (str | Path | None): Optional path to the SAP2000 executable.
        """
        pythoncom.CoInitialize()
        self.attach_to_exist: bool = attach_to_exist
        self.program_path: str | None = (
            str(Path(str(program_path)).absolute()) if program_path else None
        )
        self.mySapObject = model(
            attach_to_instance=attach_to_exist, program_path=program_path
        )
        self.SapModel = self.mySapObject.SapModel

        # Attach submodules and functions
        self.Analyze: Analyze = Analyze(mySapObject=self.mySapObject)
        self.Model: Model = Model(mySapObject=self.mySapObject)
        self.Object: Object = Object(mySapObject=self.mySapObject)
        self.Table: Table = Table(mySapObject=self.mySapObject, Model=self.Model)
        self.Load: Load = Load(mySapObject=self.mySapObject)
        self.Results: Results = Results(mySapObject=self.mySapObject)
        self.Material: Material = Material(mySapObject=self.mySapObject)
        self.Select: Select = Select(mySapObject=self.mySapObject)

        log.info("Sap2000Wrapper Initialized")

    def __str__(self) -> str:
        """Returns a string representation of the Sap2000Wrapper instance.

        Returns:
            str: Description of the wrapper instance and model type.
        """
        _attachment_str = (
            "Attached to existing Model" if self.attach_to_exist else "New Model"
        )
        return f'Instance of SAP2000Wrapper. Model type: "{_attachment_str}".'

    def __repr__(self) -> str:
        attach_to_exist = self.attach_to_exist
        return f"Sap2000Wrapper({attach_to_exist=})"

    def __del__(self) -> None:
        """@public Destructor for Sap2000Wrapper.

        Cleans up the SAP2000 object and logs any errors encountered.
        """
        try:
            # assert self.mySapObject.ApplicationExit(False) == 0
            self.SapModel = None
            self.mySapObject = None
            pythoncom.CoInitialize()
        except Exception as e:
            log.error(e.__str__())

    def save(self, savepath: str | Path | None = None) -> bool:
        """Saves the SAP model to the specified path.

        Args:
            savepath (str | Path | None): Path to save the model. If None, uses the default save location.

        Returns:
            bool: True if save was successful, False otherwise.
        """
        try:
            if savepath:
                assert self.SapModel.File.Save(savepath) == 0
                log.info(f"Save success. Saved to {savepath}")
            else:
                assert self.SapModel.File.Save() == 0
                log.info("Save success. Saved to defaultpath")
            return True
        except Exception as e:
            log.critical(e)
            return False

    @property
    def api_version(self) -> str:
        """Retrieves the API version implemented by SAP2000.

        Returns:
            str: The API version string.
        """
        return self.mySapObject.GetOAPIVersionNumber()

    def hide(self) -> bool:
        """Hides the SAP2000 application from view.

        Returns:
            bool: True if the application was successfully hidden, False otherwise.
        """
        try:
            self.mySapObject.Hide()
            return True
        except Exception as e:
            log.critical(str(e))
            return False

    def unhide(self) -> bool:
        """Unhides the SAP2000 application, making it visible again.

        Returns:
            bool: True if the application was successfully unhidden, False otherwise.
        """
        try:
            self.mySapObject.Unhide()
            return True
        except Exception as e:
            log.critical(str(e))
            return False

    @property
    def ishidden(self) -> bool:
        """Checks if the SAP2000 application is currently hidden.

        Returns:
            bool: True if hidden, False otherwise.
        """
        return self.mySapObject.Visible()

    @property
    def version(self) -> str:
        """Retrieves the version of the currently opened SAP model.

        Returns:
            str: The version of the SAP model.
        """
        return self.SapModel.GetVersion()[0]

    def exit(self, save: bool = False):
        """Exits the SAP2000 application.

        Args:
            save (bool): If True, saves the model before exiting.
        """
        self.mySapObject.ApplicationExit(False)


def model(
    attach_to_instance: bool,
    program_path: str | Path | None = None,
):
    """Creates or attaches to a SAP2000 instance.

    Args:
        attach_to_instance (bool): If True, attach to a currently running instance.
        program_path (str | Path | None): Optional specific path to SAP2000 executable.

    Returns:
        Any: The SAP2000 object.

    Raises:
        Exception: Raises an exception if the SAP2000 instance cannot be created or attached.
    """
    # create API helper object
    helper = comtypes.client.CreateObject("SAP2000v1.Helper")
    helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)

    if attach_to_instance:
        # attach to a running instance of SAP2000
        try:
            # get the active SapObject
            mySapObject = helper.GetObject("CSI.SAP2000.API.SapObject")
            log.debug("Attached to existing Instance.")
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("No running instance of the program found or failed to attach.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)
    else:
        if program_path is None:
            try:
                log.debug(
                    r"Program path not set - Looking for SAP2000.exe in C:\Program Files"
                )
                program_path = (
                    Path(r"C:\Program Files").glob("**/SAP2000.exe").__next__()
                )
            except Exception:
                _error = r"Could not locate `SAP2000.exe` in C:\Program Files"
                log.error(_error)
                raise Exception(_error + "\nTry specifying the path to SAP2000.exe")

        try:
            mySapObject = helper.CreateObject(program_path)
            mySapObject.ApplicationStart()
            mySapObject.SapModel.InitializeNewModel()  # initialize model
            log.debug(f"Created model from {program_path}.")
            return mySapObject
        except (OSError, comtypes.COMError):
            log.error("Cannot start a new instance of the program.")
            sys.exit(-1)
        except Exception as e:
            log.error(str(e))
            sys.exit(-1)
