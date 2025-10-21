from ak_sap._api.General_Functions.Helper import Helper
from .misc import eUnits


class SapObject:
    """
    Python wrapper for the SAP2000 OAPI SapObject interface.
    """

    def __init__(self, prog_id="CSI.SAP2000.API.SapObject", attach_to_existing=True):
        """
        Initializes the SapObject wrapper.

        Args:
            prog_id (str): The Program ID for the SAP2000 COM object.
                        Defaults to "CSI.SAP2000.API.SapObject".
            attach_to_existing (bool): If True, attaches to existing open SAP2000 instance
        """
        self._helper_instance: Helper = Helper()
        if attach_to_existing:
            self._SapObject = self._helper_instance.getObject(progID=prog_id)
        else:
            self._SapObject = self._helper_instance.createObjectProgID(progID=prog_id)
            self.application_start()

    def application_exit(self, file_save: bool) -> int:
        """
        Closes the Sap2000 application.

        Args:
            file_save (bool): If True, the existing model file is saved prior
                              to closing Sap2000. It's saved with its current name.

        Returns:
            int: 0 if the function succeeds, non-zero if it fails.

        Remarks:
            You should release the SapObject (e.g., set the variable to None)
            after calling this function to ensure proper cleanup.
        """
        result = self._SapObject.ApplicationExit(file_save)
        self._helper_instance = None
        print("Application exited. COM objects released.")
        return result

    def application_start(
        self,
        units: int = eUnits.kN_m_C.value,
        visible: bool = True,
        file_name: str = "",
    ) -> int:
        """
        Starts the Sap2000 application.

        Args:
            units (int): The database units used when a new model is created.
                        Use the eUnits class attributes (e.g., eUnits.kip_ft_F).
                        Defaults to kip_in_F (3).
            visible (bool): If True (default), the application is visible when started.
                            If False, the application is hidden.
            file_name (str): The full path of a model file (.sdb, .$2k, .s2k,
                            .xls, .mdb) to be opened upon start. If empty (default),
                            the application starts without loading a model.

        Returns:
            int: 0 if the application successfully starts, non-zero if it fails.
        """
        result = self._SapObject.ApplicationStart(units, visible, file_name)
        return result

    def get_oapi_version_number(self) -> float:
        """
        Retrieves the API version implemented by the running SAP2000 instance.

        Returns:
            float: The API version number of the SAP2000 program.

        Remarks:
            This version can be compared to the client/wrapper API version
            (e.g., self._helper_instance.GetOAPIVersionNumber()) to check compatibility.
        """
        return self._SapObject.GetOAPIVersionNumber()

    def hide(self) -> int:
        """
        Hides the Sap2000 application window.

        Returns:
            int: 0 if the application is successfully hidden, non-zero if it fails
                (e.g., if already hidden).

        Remarks:
            When hidden, the application is not visible on screen or in the taskbar.
        """
        return self._SapObject.Hide()

    def unhide(self) -> int:
        """
        Unhides the Sap2000 application window, making it visible.

        Returns:
            int: 0 if the application is successfully unhidden, non-zero if it fails
                (e.g., if already visible).
        """
        return self._SapObject.Unhide()

    @property
    def visible(self) -> bool:
        """
        Checks if the Sap2000 application window is currently visible.

        Returns:
            bool: True if the application is visible, False otherwise.
        """
        return self._SapObject.Visible()

    def set_as_active_object(self) -> int:
        """
        Sets the current instance of SapObject in the system Running Object Table (ROT),
        replacing any previous instance.

        Returns:
            int: 0 if the instance is successfully set as active in the ROT,
                non-zero if it fails.

        Remarks:
            Allows other processes to attach to this specific instance using GetObject().
            Newly created SapObjects are often automatically added if none exists.
            This method ensures *this* instance is the active one.
        """
        return self._SapObject.SetAsActiveObject()

    def unset_as_active_object(self) -> int:
        """
        Removes the current instance of SapObject from the system Running Object Table (ROT).

        Returns:
            int: 0 if the instance is successfully removed from the ROT,
                non-zero if it fails or if the instance was not in the ROT.
        """
        return self._SapObject.UnsetAsActiveObject()
