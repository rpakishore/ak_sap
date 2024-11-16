from ak_sap.utils import MasterClass
from ak_sap.utils.decorators import smooth_sap_do


class Ritz(MasterClass):
    def __init__(self, mySapObject) -> None:
        super().__init__(mySapObject=mySapObject)
        assert self.SapModel is not None
        self.ModalRitz = self.SapModel.LoadCases.ModalRitz

    def __str__(self) -> str:
        return f"Instance of `Loads.Modal.{self.__class__.__name__}`. Holds collection of functions"

    @smooth_sap_do
    def get_initial_case(self, case_name: str) -> str:
        """retrieves the initial condition assumed for the specified load case.

        Response: This is blank, None, or the name of an existing analysis case.
        This item specifies if the load case starts from zero initial conditions, that is, an unstressed state, or if it starts using the stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history load case.
        If the specified initial case is a nonlinear static or nonlinear direct integration time history load case, the stiffness at the end of that case is used.
        If the initial case is anything else, zero initial conditions are assumed.
        """
        return self.ModalRitz.GetInitialCase(case_name)

    @smooth_sap_do
    def set_initial_case(self, case_name: str, initial_case: str):
        """sets the initial condition for the specified load case.
        `initial_case` lets you use stiffness that occurs at the end of a nonlinear static or nonlinear direct integration time history load case.
        """
        return self.ModalRitz.SetInitialCase(case_name, initial_case)

    @smooth_sap_do
    def get_loads(self, case_name: str) -> dict:
        """retrieves the load data for the specified load case."""
        _ret: tuple = self.ModalRitz.GetLoads(case_name)
        _values: dict = {
            "NumberOfLoads": _ret[0],
            "LoadType": _ret[1],
            "LoadName": _ret[2],
            "RitzMaxCycles": _ret[3],
            "TargetParticipationRatio": _ret[4],
        }
        return _values, 0  # type: ignore

    @smooth_sap_do
    def get_number_modes(self, case_name: str) -> tuple[int]:
        """retrieves the max and min number of modes requested for the specified load case."""
        return self.ModalRitz.GetNumberModes(case_name)

    @smooth_sap_do
    def set_number_modes(self, case_name: str, max: int, min: int):
        """sets the number of modes requested for the specified load case."""
        return self.ModalRitz.SetNumberModes(case_name, max, min)

    @smooth_sap_do
    def set_case(self, case_name: str):
        """Initializes a modal eigen load case.
        If this function is called for an existing load case, all items for the case are reset to their default value
        """
        return self.ModalRitz.SetCase(case_name)
