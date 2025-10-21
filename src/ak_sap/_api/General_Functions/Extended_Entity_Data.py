from ak_sap._api.General_Functions.SapModel import SapModel


class ExtendedEntityData:
    def __init__(self, sap: SapModel):
        self.SapModel = sap

    def get_key_strings_extended_entity_data(
        self, app_name: str, key: str
    ) -> tuple[int, int, tuple[str, ...]]:
        """
        Retrieves string data previously stored for a specific application and key.

        Args:
            app_name (str): The application name under which the data was stored.
                            Comparison is case-insensitive and culturally invariant.
            key (str): The entry name (key) under which the data was stored.
                       Comparison is case-insensitive and culturally invariant.

        Returns:
            Tuple[int, int, Tuple[str, ...]]:
                - int: 0 if the function call is successful, non-zero otherwise.
                - int: The number of string values retrieved (NumberValues).
                - Tuple[str, ...]: A tuple containing the string values stored
                                   under the specified application name and key.
                                   Returns an empty tuple if no data exists or
                                   on failure.

        Based on VBA Documentation: GetKeyStringsExtendedEntityData
        Syntax: SapObject.SapModel.GetKeyStringsExtendedEntityData(AppName, Key, NumberValues, Values)
        """

        _number_values = 0
        _values = []

        result = self.sap_model.GetKeyStringsExtendedEntityData(
            app_name, key, _number_values, _values
        )

        ret_code = result[0]
        number_values_out = result[1]
        values_out = result[2] if result[2] is not None else tuple()

        # Ensure values_out is always a tuple, even if empty or None was returned
        if not isinstance(values_out, tuple):
            # Handle cases where comtypes might return a list or other sequence
            try:
                values_out = tuple(values_out)
            except TypeError:
                values_out = tuple()  # Fallback to empty tuple if conversion fails

        return ret_code, number_values_out, values_out
