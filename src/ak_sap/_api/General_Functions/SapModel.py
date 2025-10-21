from ak_sap._api.General_Functions.SapObject import SapObject
from .misc import eUnits


class SapModel:
    def __init__(
        self, sapobject: SapObject | None = None, attach_to_existing: bool = True
    ):
        """
        Initializes the SapModelWrapper.

        Args:
            sapobject: An optional existing SapObject instance. If None, a new
                       SapObject will be created.
            attach_to_existing: If creating a new SapObject, specifies whether
                                to attach to an existing SAP2000 instance (True)
                                or start a new one (False). Defaults to True.
        """
        if sapobject is None:
            self.SapObject = SapObject(attach_to_existing=attach_to_existing)
        else:
            self.SapObject = sapobject

    @property
    def SapModel(self):
        return self.SapObject._SapObject.SapModel

    def _handle_error(self, return_code: int, function_name: str):
        """Helper function to raise an error if the API call failed."""
        if return_code != 0:
            raise RuntimeError(
                f"SAP API call {function_name} failed with error code: {return_code}"
            )

    def get_database_units(self) -> eUnits:
        """
        Returns the database units for the model.

        All data is internally stored in the model in these units and converted
        to the present units as needed.

        Returns:
            eUnits: An enum member indicating the database units.
        """
        unit_value = self.SapModel.GetDatabaseUnits()
        return eUnits(unit_value)

    def get_merge_tol(self) -> float:
        """
        Retrieves the value of the program auto merge tolerance.

        Returns:
            float: The program auto merge tolerance in the current length units [L].

        Raises:
            RuntimeError: If the API call fails.
        """
        ret, merge_tol = self.SapModel.GetMergeTol()
        self._handle_error(ret, "GetMergeTol")
        return merge_tol

    def get_model_filename(self, include_path: bool = True) -> str:
        """
        Returns the filename of the current model.

        Args:
            include_path (bool, optional): If True, the returned filename includes
                                           the full path. Defaults to True.

        Returns:
            str: The filename of the current model, with or without the full path.
        """
        return self.SapModel.GetModelFilename(include_path)

    def get_model_filepath(self) -> str:
        """
        Returns the filepath (directory) of the current model.

        Returns:
            str: The filepath where the current model is saved.
        """
        return self.SapModel.GetModelFilepath()

    def get_model_is_locked(self) -> bool:
        """
        Checks if the model is locked.

        With some exceptions, definitions and assignments cannot be changed
        while the model is locked.

        Returns:
            bool: True if the model is locked, False otherwise.
        """
        return self.SapModel.GetModelIsLocked()

    def get_notional_size(self, name: str) -> tuple[str, float]:
        """
        Retrieves the method and value used to determine the notional size
        of a shell-type area section for creep and shrinkage calculations.

        Args:
            name (str): The name of an existing shell-type area section property.

        Returns:
            Tuple[str, float]: A tuple containing:
                - stype (str): The type defining the notional size ("Auto", "User", "None").
                - value (float): The scale factor (for "Auto"), the user-defined
                                 size [L] (for "User"), or 1 (for "None").

        Raises:
            RuntimeError: If the API call fails.
        """
        ret, stype, value = self.SapModel.PropArea.GetNotionalSize(name)
        self._handle_error(ret, f"PropArea.GetNotionalSize(Name='{name}')")
        return stype, value

    def get_present_coord_system(self) -> str:
        """
        Returns the name of the present coordinate system.

        Returns:
            str: The name of the current coordinate system (e.g., "GLOBAL").
        """
        return self.SapModel.GetPresentCoordSystem()

    def get_present_units(self) -> eUnits:
        """
        Returns the units presently specified for the model display and input/output.

        Returns:
            eUnits: An enum member indicating the present units.
        """
        unit_value = self.SapModel.GetPresentUnits()
        return eUnits(unit_value)

    def get_project_info(self) -> dict[str, str]:
        """
        Retrieves the project information data as a dictionary.

        Returns:
            Dict[str, str]: A dictionary where keys are the project info item names
                            and values are the corresponding data.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret, number_items, items, data = self.SapModel.GetProjectInfo()
        self._handle_error(ret, "GetProjectInfo")
        # Ensure items and data are lists/tuples before zipping
        if not isinstance(items, (list, tuple)):
            items = []
        if not isinstance(data, (list, tuple)):
            data = []
        # Handle potential mismatch if API returns inconsistent lengths (unlikely but safe)
        min_len = min(len(items), len(data))
        return dict(zip(items[:min_len], data[:min_len]))

    def get_user_comment(self) -> str:
        """
        Retrieves the data in the user comments and log.

        Returns:
            str: The content of the user comments and log.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret, comment = self.SapModel.GetUserComment()
        self._handle_error(ret, "GetUserComment")
        return comment

    def get_version(self) -> tuple[str, float]:
        """
        Returns the SAP2000 program version information.

        Returns:
            Tuple[str, float]: A tuple containing:
                - version_string (str): The program version name (e.g., "SAP2000 v25.0.0").
                - version_number (float): The internal program version number.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret, version_str, version_num = self.SapModel.GetVersion()
        self._handle_error(ret, "GetVersion")
        return version_str, version_num

    def initialize_new_model(self, units: eUnits = eUnits.kip_in_F) -> None:
        """
        Clears the previous model and initializes the program for a new model.

        Warning: Unsaved changes in the current model will be lost.

        Args:
            units (eUnits, optional): The database units for the new model.
                                      Defaults to eUnits.kip_in_F.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret = self.SapModel.InitializeNewModel(units.value)
        self._handle_error(ret, f"InitializeNewModel(Units={units.name})")
        print(f"New model initialized with database units: {units.name}")

    def set_merge_tol(self, merge_tol: float) -> None:
        """
        Sets the program auto merge tolerance.

        Args:
            merge_tol (float): The desired auto merge tolerance in current length units [L].

        Raises:
            RuntimeError: If the API call fails (e.g., model is locked).
        """
        ret = self.SapModel.SetMergeTol(merge_tol)
        self._handle_error(ret, f"SetMergeTol(MergeTol={merge_tol})")
        print(f"Merge tolerance set to: {merge_tol}")

    def set_model_is_locked(self, lock_it: bool) -> None:
        """
        Locks or unlocks the model.

        Args:
            lock_it (bool): True to lock the model, False to unlock it.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret = self.SapModel.SetModelIsLocked(lock_it)
        self._handle_error(ret, f"SetModelIsLocked(LockIt={lock_it})")
        print(f"Model lock status set to: {lock_it}")

    def set_notional_size(self, name: str, stype: str, value: float) -> None:
        """
        Assigns the method and value to determine the notional size of a
        shell-type area section for creep and shrinkage calculations.

        Args:
            name (str): The name of an existing shell-type area section property.
            stype (str): The type to define the notional size ("Auto", "User", "None").
            value (float): The scale factor (for "Auto"), the user-defined
                           size [L] (for "User"), or 1 (for "None").

        Raises:
            RuntimeError: If the API call fails.
            ValueError: If stype is not one of the allowed values.
        """
        allowed_stypes = ["Auto", "User", "None"]
        if stype not in allowed_stypes:
            raise ValueError(
                f"Invalid stype '{stype}'. Must be one of {allowed_stypes}"
            )

        ret = self.SapModel.PropArea.SetNotionalSize(name, stype, value)
        self._handle_error(
            ret,
            f"PropArea.SetNotionalSize(Name='{name}', stype='{stype}', Value={value})",
        )
        print(f"Notional size for '{name}' set to type '{stype}', value {value}")

    def set_present_coord_system(self, csys: str) -> None:
        """
        Sets the present coordinate system for display and input/output.

        Args:
            csys (str): The name of a defined coordinate system (e.g., "GLOBAL", "CSys1").

        Raises:
            RuntimeError: If the API call fails (e.g., coordinate system not found).
        """
        ret = self.SapModel.SetPresentCoordSystem(csys)
        self._handle_error(ret, f"SetPresentCoordSystem(CSys='{csys}')")
        print(f"Present coordinate system set to: {csys}")

    def set_present_units(self, units: eUnits) -> None:
        """
        Sets the units presently specified for the model display and input/output.

        Args:
            units (eUnits): The desired present units enum member.

        Raises:
            RuntimeError: If the API call fails.
        """
        ret = self.SapModel.SetPresentUnits(units.value)
        self._handle_error(ret, f"SetPresentUnits(Units={units.name})")
        print(f"Present units set to: {units.name}")

    def set_project_info(self, item: str, data: str) -> None:
        """
        Sets the data for an item in the project information.

        Args:
            item (str): The name of the project information item (e.g., "Project Name").
            data (str): The data value for the specified item.

        Raises:
            RuntimeError: If the API call fails (e.g., model is locked).
        """
        ret = self.SapModel.SetProjectInfo(item, data)
        self._handle_error(ret, f"SetProjectInfo(Item='{item}')")
        print(f"Project info item '{item}' set.")

    def set_user_comment(
        self, comment: str, num_lines: int = 1, replace: bool = False
    ) -> None:
        """
        Sets or adds to the user comments and log data.

        Args:
            comment (str): The comment text to add or set.
            num_lines (int, optional): The number of blank lines to add before the
                                       comment when appending. Ignored if replace=True
                                       or if comments are initially empty. Defaults to 1.
            replace (bool, optional): If True, all existing comments are replaced
                                      with the specified comment. Defaults to False.

        Raises:
            RuntimeError: If the API call fails (e.g., model is locked).
        """
        ret = self.SapModel.SetUserComment(comment, num_lines, replace)
        self._handle_error(ret, f"SetUserComment(Replace={replace})")
        print(f"User comment {'set' if replace else 'added'}.")
