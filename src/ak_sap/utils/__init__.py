"""Initialize the utils module.

This module includes various utility functions and classes that support 
the main functionality of the ak_sap package.
"""

from .logger import log


class MasterClass:
    """A base class for modules interacting with the SAP2000 API.

    This class provides a standard interface for accessing the SAP2000
    model and logging functionalities.

    Attributes:
        mySapObject: The main SAP2000 object.
        SapModel: The SAP2000 model object.
    """

    def __init__(self, mySapObject) -> None:
        """Initializes the MasterClass.

        Args:
            mySapObject: The main SAP2000 object to interface with.
        """
        self.mySapObject = mySapObject
        self.SapModel = self.mySapObject.SapModel
        print(f"`{self.__class__.__name__}` instance initialized.")

    def __str__(self) -> str:
        return f"Instance of `Loads.Modal.{self.__class__.__name__}`. Holds collection of functions"

    def __repr__(self) -> str:
        return self.__str__()

    def __del__(self) -> None:
        try:
            self.mySapObject = None
            self.SapModel = None
        except Exception as e:
            log.warning(
                msg=f"Exception faced when deleting {self.__class__.__name__}\n{e}"
            )
